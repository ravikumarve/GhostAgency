"""Tests for settings database and settings page routes."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from ghostagency.api.main import create_app
from ghostagency.core import settings_db


# =========================================================================
# Settings DB unit tests
# =========================================================================

class TestSettingsDB:
    """Tests for the SQLite-backed settings store."""

    def setup_method(self):
        settings_db.clear()

    def test_get_default_none(self):
        assert settings_db.get("nonexistent") is None

    def test_get_falls_back_to_env(self):
        os.environ["TEST_GHOST_VAR"] = "from_env"
        val = settings_db.get("test_ghost_var")
        assert val == "from_env"
        del os.environ["TEST_GHOST_VAR"]

    def test_set_and_get(self):
        settings_db.set("my_key", "my_value")
        assert settings_db.get("my_key") == "my_value"

    def test_set_overwrites(self):
        settings_db.set("key", "v1")
        settings_db.set("key", "v2")
        assert settings_db.get("key") == "v2"

    def test_db_overrides_env(self):
        os.environ["OVERRIDE_TEST"] = "env_val"
        settings_db.set("override_test", "db_val")
        assert settings_db.get("override_test") == "db_val"
        del os.environ["OVERRIDE_TEST"]
        settings_db.delete("override_test")

    def test_delete(self):
        settings_db.set("temp", "x")
        assert settings_db.get("temp") == "x"
        settings_db.delete("temp")
        assert settings_db.get("temp") is None

    def test_clear_all(self):
        settings_db.set("a", "1")
        settings_db.set("b", "2")
        settings_db.clear()
        assert settings_db.get("a") is None
        assert settings_db.get("b") is None

    def test_set_many(self):
        settings_db.set_many({"k1": "v1", "k2": "v2"})
        assert settings_db.get("k1") == "v1"
        assert settings_db.get("k2") == "v2"
        settings_db.delete("k1")
        settings_db.delete("k2")

    def test_get_all(self):
        settings_db.set("x", "1")
        settings_db.set("y", "2")
        all_s = settings_db.get_all()
        assert "x" in all_s
        assert "y" in all_s
        settings_db.clear()

    def test_get_by_prefix(self):
        settings_db.set_many({"openai_key": "sk-...", "openai_model": "gpt-4", "other": "x"})
        prefixed = settings_db.get_by_prefix("openai")
        assert "openai_key" in prefixed
        assert "openai_model" in prefixed
        assert "other" not in prefixed
        settings_db.clear()

    def test_get_effective_merges_env_and_db(self):
        os.environ["EFF_TEST"] = "env_val"
        settings_db.set("eff_test", "db_val")
        eff = settings_db.get_effective()
        assert eff.get("eff_test") == "db_val"  # DB wins
        settings_db.delete("eff_test")
        eff2 = settings_db.get_effective()
        assert eff2.get("eff_test") == "env_val"  # env fallback
        del os.environ["EFF_TEST"]

    def test_get_int_default(self):
        assert settings_db.get_int("missing") == 0
        assert settings_db.get_int("missing", 42) == 42
        settings_db.set("num", "7")
        assert settings_db.get_int("num") == 7
        settings_db.delete("num")

    def test_get_bool_default(self):
        assert settings_db.get_bool("missing") is False
        settings_db.set("flag", "true")
        assert settings_db.get_bool("flag") is True
        settings_db.set("flag", "True")
        assert settings_db.get_bool("flag") is True
        settings_db.set("flag", "1")
        assert settings_db.get_bool("flag") is True
        settings_db.delete("flag")


# =========================================================================
# Settings page route tests
# =========================================================================

class TestSettingsRoutes:
    """Tests for the /settings page."""

    @pytest.fixture
    def client(self):
        return TestClient(create_app())

    @pytest.fixture
    def headers(self):
        return {"Authorization": "Bearer test-license"}

    def test_get_settings_returns_page(self, client, headers):
        with patch("ghostagency.api.middleware.auth.validate_license_key", return_value=True):
            resp = client.get("/settings", headers=headers)
            assert resp.status_code == 200
            assert "SETTINGS" in resp.text
            assert "LLM Provider" in resp.text
            assert "Agent Runtime" in resp.text
            assert "Notifications" in resp.text
            assert "Billing" in resp.text

    def test_post_settings_saves_and_shows_banner(self, client, headers):
        with patch("ghostagency.api.middleware.auth.validate_license_key", return_value=True):
            resp = client.post(
                "/settings",
                data={"llm_provider": "gemini", "gemini_model": "gemini-2.0-flash"},
                headers=headers,
            )
            assert resp.status_code == 200
            assert "SETTINGS SAVED" in resp.text
            assert settings_db.get("llm_provider") == "gemini"
            assert settings_db.get("gemini_model") == "gemini-2.0-flash"
            settings_db.delete("llm_provider")
            settings_db.delete("gemini_model")

    def test_post_settings_empty_body(self, client, headers):
        with patch("ghostagency.api.middleware.auth.validate_license_key", return_value=True):
            resp = client.post("/settings", data={}, headers=headers)
            assert resp.status_code == 200
            # Should render page without error
            assert "SETTINGS" in resp.text
