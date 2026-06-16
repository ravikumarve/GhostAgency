# Ghost Agency — Acquire.com Exit Roadmap

> **Goal:** Take Ghost Agency from localhost prototype → revenue-generating SaaS → Acquire.com listing → successful acquisition.
> **Current state:** 6/156 agents, $0 MRR, localhost only, 8/64 requirements met (12.5%).
> **Target state:** 10+ agents, $500+ MRR, live HTTPS deployment, 50+/64 requirements met (80%+).
> **Estimated timeline:** 6-8 weeks to Acquire-ready. 12-16 weeks to optimal exit.
> **Last updated:** 2026-06-16

---

## PHASE 1: SHIP IT LIVE (Week 1-2)

> **Goal:** Get a working product on a public HTTPS URL with a custom domain.
> **Why:** Without a live site, you can't create an Acquire account, connect GA4, or accept paying customers. This is the #1 blocker for everything.

### 1.1 Cloud Deployment

| Task | Details | Effort | Status |
|---|---|---|---|
| Deploy to Railway or Render | Both have free tiers. Railway is simpler for FastAPI. Push from GitHub → auto-deploy. | 2h | ⬜ |
| Set `GHOST_MOCK_AI=true` for demo | Ensure the live demo works without NIM API key (buyers test it). | 15min | ⬜ |
| Configure environment variables | Set all env vars in Railway/Render dashboard from `.env.example`. | 30min | ⬜ |
| Verify all routes return 200 | Test `/`, `/agents`, `/squads`, `/health`, `/settings`, `/dashboard`. | 30min | ⬜ |
| Set up auto-deploy from `main` branch | Push to GitHub → Railway rebuilds. CI/CD for free. | 15min | ⬜ |

### 1.2 Domain & SSL

| Task | Details | Effort | Status |
|---|---|---|---|
| Buy domain | `ghostagency.ai` or `ghostagency.io` (~$10-20/yr from Porkbun/Namecheap). | 15min | ⬜ |
| Point DNS to Railway/Render | Add CNAME record in domain registrar. | 15min | ⬜ |
| Verify SSL certificate | Railway/Render auto-provision SSL. Verify `https://` works. | 5min | ⬜ |
| Add domain to FastAPI CORS whitelist | Update `allow_origins` in `api/main.py` from `["*"]` to specific domains. | 15min | ⬜ |

### 1.3 Analytics Setup

| Task | Details | Effort | Status |
|---|---|---|---|
| Create GA4 property | Google Analytics 4 — free. Add tracking ID to base.html template. | 30min | ⬜ |
| Add GA4 script to `templates/base.html` | Insert gtag.js in `<head>`. | 15min | ⬜ |
| Verify data flowing | Visit site, check Real-Time report in GA4. | 15min | ⬜ |
| Connect GA4 to Acquire.com | Done later when creating listing, but set up the data flow now. | 15min | ⬜ |

### 1.4 Legal Pages

| Task | Details | Effort | Status |
|---|---|---|---|
| Create `/privacy` route + template | Privacy policy page. Use a generator like termly.io or privacypolicies.com. | 1h | ⬜ |
| Create `/terms` route + template | Terms of service page. | 1h | ⬜ |
| Add cookie consent banner | Simple CSS-only banner in `base.html`. Required for EU/GDPR. | 30min | ⬜ |
| Add footer links to privacy/terms | Update `templates/base.html` footer. | 15min | ⬜ |

**Phase 1 Exit Criteria:**
- [ ] `https://ghostagency.ai` returns 200 with valid SSL
- [ ] GA4 shows real-time visitors
- [ ] Privacy policy and ToS pages are live
- [ ] All dashboard routes work on production URL

---

## PHASE 2: MONETIZE IT (Week 2-4)

> **Goal:** Accept real payments. Get first paying customers. Move from "pre-revenue" to "early traction."
> **Why:** $0 MRR = likely Acquire rejection. Even $100 MRR transforms your listing from "probably rejected" to "probably listed." $500 MRR = competitive listing.

### 2.1 Stripe Integration

| Task | Details | Effort | Status |
|---|---|---|---|
| Create Stripe account | stripe.com — free to create, pay-as-you-go (2.9% + 30¢ per transaction). | 30min | ⬜ |
| Create 3 products in Stripe | Starter ($97/mo), Pro ($297/mo), Enterprise ($997/mo). | 30min | ⬜ |
| Build `integrations/stripe_client.py` | Stripe Checkout session creation + webhook handler for `checkout.session.completed`. | 3h | ⬜ |
| Add `/pricing` route + template | Pricing page with Stripe Checkout buttons. | 2h | ⬜ |
| Add `/checkout/success` + `/checkout/cancel` routes | Post-payment redirect pages. | 1h | ⬜ |
| Add Stripe webhook endpoint | `/api/v1/stripe/webhook` — verifies signature, updates customer status. | 2h | ⬜ |
| Store customer data in SQLite | Extend `settings_db.py` or create `customers_db.py` — email, plan, stripe_customer_id, status. | 2h | ⬜ |
| Replace Gumroad stub with Stripe | Update `integrations/gumroad.py` → `integrations/license.py` using Stripe customer lookup. | 1h | ⬜ |
| Test full payment flow | Buy with Stripe test card (4242 4242 4242 4242). Verify webhook fires. | 1h | ⬜ |

### 2.2 Landing Page Conversion

| Task | Details | Effort | Status |
|---|---|---|---|
| Add CTA buttons to landing page | "Get Started" → `/pricing`. "Book Demo" → Calendly link. | 1h | ⬜ |
| Add pricing section to landing page | 3-tier pricing cards below the fold. | 1h | ⬜ |
| Add social proof section | "Trusted by X businesses" — even placeholder for now. | 30min | ⬜ |
| Add FAQ section | Address common buyer objections. | 1h | ⬜ |
| Add email capture form | For visitors not ready to buy. Store in SQLite. | 1h | ⬜ |

### 2.3 Customer Onboarding

| Task | Details | Effort | Status |
|---|---|---|---|
| Build first-run wizard | After signup: choose industry → select agents → configure KB → deploy. | 4h | ⬜ |
| Add welcome email (SMTP) | Build `integrations/email_smtp.py`. Send onboarding email after Stripe payment. | 3h | ⬜ |
| Add user dashboard | Show active agents, usage stats, billing status. | 3h | ⬜ |
| Add KB upload interface | Let customers upload their knowledge base files. | 2h | ⬜ |

### 2.4 Get First Customers

| Task | Details | Effort | Status |
|---|---|---|---|
| List on Product Hunt | Launch as "AI Employee Platform for SMBs." | 2h prep | ⬜ |
| Post in r/SaaS, r/smallbusiness | Genuine value post, not spam. | 30min | ⬜ |
| Cold email 20 local businesses | "AI customer support agent for $97/mo — replaces a $3,000/mo employee." | 2h | ⬜ |
| Offer 14-day free trial | Reduce friction to first signup. | 30min | ⬜ |
| Target: 3 paying customers | Even at $97/mo = $291 MRR. This changes everything. | Ongoing | ⬜ |

**Phase 2 Exit Criteria:**
- [ ] Stripe Checkout works end-to-end (test + live mode)
- [ ] At least 1 paying customer (target: 3)
- [ ] MRR ≥ $97 (target: $291)
- [ ] Pricing page live at `/pricing`
- [ ] Email onboarding flow works

---

## PHASE 3: COMPLETE THE PRODUCT (Week 3-5)

> **Goal:** Remove all stubs, TODOs, and placeholder code. Fill missing squad directories. Make the product feel finished.
> **Why:** Buyers see stubs as hidden work they'll have to do. Every TODO is a price reduction. A complete product commands a premium.

### 3.1 Missing Squads (Minimum 1 Agent Each)

| Task | Details | Effort | Status |
|---|---|---|---|
| Create `squad_data/` directory + `data_research.py` | Data Research Agent — `run_analysis()` primary action. | 2h | ⬜ |
| Create `squad_dev/` directory + `dev_code_review.py` | Code Review Agent — `assist_dev()` primary action. | 2h | ⬜ |
| Create `squad_finance/` directory + `finance_invoicing.py` | Invoicing Agent — `process_task()` primary action. | 2h | ⬜ |
| Create `squad_hr/` directory + `hr_recruiting.py` | Recruiting Agent — `handle_hr_task()` primary action. | 2h | ⬜ |
| Create `squad_legal/` directory + `legal_contract_review.py` | Contract Review Agent — `review_document()` primary action. | 2h | ⬜ |
| Create `squad_custom/` directory + `custom_generic.py` | Custom Agent — `custom_action()` primary action. | 1h | ⬜ |
| Register all 6 new agents in `agent_registry.py` | Update `TOTAL_AGENTS = 12`. Add imports + registry entries. | 30min | ⬜ |
| Write tests for each new squad | One test file per squad in `tests/squads/`. | 3h | ⬜ |
| Run `validate_registry.py` | Confirm 12 agents registered. | 5min | ⬜ |

### 3.2 Missing Integrations

| Task | Details | Effort | Status |
|---|---|---|---|
| Build `integrations/email_smtp.py` | SMTP email sending (escalation, notifications, onboarding). | 3h | ⬜ |
| Build `integrations/webhook.py` | Generic webhook dispatcher for external notifications. | 2h | ⬜ |
| Build `integrations/telegram_bot.py` | Telegram bot for mobile alerts and agent interaction. | 3h | ⬜ |
| Build `kb/cache.py` | In-memory KB cache — load once, reuse across calls. | 1h | ⬜ |
| Build `kb/chunker.py` | Separate chunker module (currently in `loader.py`). | 1h | ⬜ |

### 3.3 Missing Core Components

| Task | Details | Effort | Status |
|---|---|---|---|
| Build `core/squad_router.py` | Intelligent task → squad routing. Match task keywords to squad capabilities. | 3h | ⬜ |
| Build `scripts/benchmark.py` | Response time benchmarks per squad. | 2h | ⬜ |
| Fix `/metrics` endpoint | Replace hardcoded data with real metrics (uptime, request count, latency, agent usage). | 2h | ⬜ |
| Remove Gumroad stub completely | Replace `gumroad.py` with `license.py` backed by Stripe. | 1h | ⬜ |
| Remove all `# TODO` comments | Search codebase for TODOs. Either implement or delete. | 2h | ⬜ |

### 3.4 Quality Hardening

| Task | Details | Effort | Status |
|---|---|---|---|
| Add GitHub Actions CI | On push to main: run `black`, `flake8`, `pytest`. | 2h | ⬜ |
| Add Dependabot | Auto-PR for dependency updates. | 15min | ⬜ |
| Add `safety check` to CI | Scan for known vulnerabilities in dependencies. | 30min | ⬜ |
| Clean up root debris | Delete `nohup.out`, `server.log`. Add to `.gitignore`. | 15min | ⬜ |
| Make repo public | Buyers need to verify the codebase. Private repos raise suspicion. | Decision | ⬜ |
| Full test suite pass | `pytest --tb=short -q` — all green. | 30min | ⬜ |

**Phase 3 Exit Criteria:**
- [ ] All 10 squad directories exist with at least 1 agent each
- [ ] `TOTAL_AGENTS = 12` (or more), all registered and tested
- [ ] Zero `# TODO` comments in production code
- [ ] Zero stub/placeholder functions
- [ ] CI/CD pipeline green on GitHub Actions
- [ ] `squad_router.py` routes tasks to correct squads
- [ ] All 3 integrations (email, webhook, telegram) functional

---

## PHASE 4: ACQUISITION-READY PACKAGE (Week 5-6)

> **Goal:** Create every document, video, and artifact a buyer needs to evaluate and acquire Ghost Agency.
> **Why:** Acquire.com's Listing Scorecard rewards sellers who provide CIM, P&L, demo video, and transition plan. These directly increase buyer interest and sale price.

### 4.1 Confidential Information Memorandum (CIM)

The CIM is the #1 document buyers request. It tells the story of your business.

| Section | Content | Effort | Status |
|---|---|---|---|
| Executive Summary | 1-page overview: what it does, who it's for, why it's valuable. | 1h | ⬜ |
| Business Model | SaaS pricing tiers, unit economics, cost structure. | 1h | ⬜ |
| Product Overview | Feature list, architecture, tech stack, agent catalog. | 1h | ⬜ |
| Market Opportunity | TAM/SAM/SOM for AI Employee market. Competitor analysis. | 2h | ⬜ |
| Growth Levers | What a buyer could do to 10x the business. | 1h | ⬜ |
| Risk Assessment | Honest assessment of risks and mitigants. | 1h | ⬜ |
| Financial Summary | MRR, churn, LTV, CAC — even 2-3 months of data. | 1h | ⬜ |

### 4.2 Profit & Loss Statement (P&L)

| Task | Details | Effort | Status |
|---|---|---|---|
| Create P&L spreadsheet | Monthly revenue, costs (hosting, API, email), profit. Even 2-3 months. | 2h | ⬜ |
| Upload to Acquire listing | Use their P&L Builder tool. | 30min | ⬜ |
| Connect Stripe to ChartMogul | Auto-syncs MRR, churn, LTV to your Acquire listing. | 1h | ⬜ |

### 4.3 Demo & Intro Videos

| Task | Details | Effort | Status |
|---|---|---|---|
| Record 5-min product demo | Walk through: landing page → pricing → dashboard → agent execution → settings. | 2h | ⬜ |
| Record 2-min founder intro | Who you are, why you built it, what makes it special. | 1h | ⬜ |
| Upload both to Acquire listing | Videos dramatically increase buyer engagement. | 15min | ⬜ |

### 4.4 Transition & Operations Documentation

| Task | Details | Effort | Status |
|---|---|---|---|
| Write 30-day transition plan | Week 1: Knowledge transfer. Week 2: Shadow operations. Week 3: Buyer-led. Week 4: Handoff complete. | 2h | ⬜ |
| Write ops runbook | How to deploy, monitor, debug, scale, handle incidents. | 3h | ⬜ |
| Write architecture docs | C4 diagrams: Context → Container → Component → Code. | 3h | ⬜ |
| Write customer support playbook | How to handle support requests, escalations, refunds. | 1h | ⬜ |
| Write marketing playbook | Channels that work, ad copy, email templates, SEO strategy. | 2h | ⬜ |
| Document all 3rd-party dependencies | Licenses, API keys needed, monthly costs per service. | 1h | ⬜ |

### 4.5 Data Room Preparation

| Document | Purpose | Status |
|---|---|---|
| CIM (Confidential Information Memorandum) | Business overview for serious buyers | ⬜ |
| P&L statement (2-3 months minimum) | Financial verification | ⬜ |
| Bank statements | Revenue reconciliation | ⬜ |
| Stripe reports | Independent revenue verification | ⬜ |
| Customer list (anonymized) | Shows customer base health | ⬜ |
| Code repository access | Technical due diligence | ⬜ |
| Architecture diagrams | System understanding | ⬜ |
| Transition plan | Post-acquisition operations | ⬜ |
| IP assignment template | Legal transfer of code ownership | ⬜ |
| Vendor/dependency list | Ongoing cost obligations | ⬜ |

**Phase 4 Exit Criteria:**
- [ ] CIM written and reviewed
- [ ] P&L uploaded to Acquire
- [ ] Demo video recorded and uploaded
- [ ] Transition plan documented
- [ ] Data room fully populated
- [ ] All Listing Scorecard items checked

---

## PHASE 5: LIST & SELL (Week 6-8)

> **Goal:** Create the Acquire.com listing, field buyer inquiries, negotiate, and close.
> **Why:** This is the finish line. Everything before this was preparation.

### 5.1 Create Acquire.com Listing

| Task | Details | Effort | Status |
|---|---|---|---|
| Create seller account | Sign up at acquire.com. Verify email + identity. | 30min | ⬜ |
| Set asking price | Based on MRR × multiple. If $500 MRR at 5x ARR = $30,000. | 30min | ⬜ |
| Write listing headline | "AI Employee SaaS — 10+ Specialized Agents, $X MRR, 99% Margins" | 30min | ⬜ |
| Write listing description | Problem, solution, traction, growth levers, tech stack. | 2h | ⬜ |
| Connect GA4 metrics | Acquire verifies traffic data. | 15min | ⬜ |
| Connect Stripe/ChartMogul | Acquire verifies revenue data. | 15min | ⬜ |
| Upload CIM, P&L, demo video | Populate the data room. | 30min | ⬜ |
| Submit for curation review | Acquire's team reviews within 24-48 hours. | 5min | ⬜ |

### 5.2 Field Buyer Inquiries

| Task | Details | Effort | Status |
|---|---|---|---|
| Screen buyers (proof of funds) | Don't share data room with unqualified buyers. | Ongoing | ⬜ |
| Respond within 24 hours | Fast response = more serious offers. | Ongoing | ⬜ |
| Schedule buyer calls | 30-min intro calls with serious buyers. | Ongoing | ⬜ |
| Request NDAs before data room access | Protect your IP. | Ongoing | ⬜ |

### 5.3 Negotiate & Close

| Task | Details | Effort | Status |
|---|---|---|---|
| Evaluate LOIs (Letter of Intent) | Compare price, terms, earn-out structure, transition support. | Ongoing | ⬜ |
| Negotiate best offer | Don't accept first offer. Create FOMO with multiple buyers. | Ongoing | ⬜ |
| Set up escrow via Acquire.com | Built-in escrow protects both parties. | 1h | ⬜ |
| Transfer assets | Domain, code, Stripe account, customer data, infrastructure. | 1-2 days | ⬜ |
| 30-day transition support | Help buyer operate the business. | 30 days | ⬜ |

**Phase 5 Exit Criteria:**
- [ ] Listing live on Acquire.com
- [ ] 25+ buyer inquiries (Acquire average)
- [ ] At least 1 LOI received
- [ ] Deal closed via escrow

---

## TIMELINE SUMMARY

```
Week 1-2:  PHASE 1 — Ship It Live
           Deploy → Domain → SSL → GA4 → Legal Pages
           
Week 2-4:  PHASE 2 — Monetize It
           Stripe → Pricing → Landing CTA → First Customers → $500 MRR target
           
Week 3-5:  PHASE 3 — Complete the Product
           6 Missing Squads → Integrations → Squad Router → Remove Stubs → CI/CD
           
Week 5-6:  PHASE 4 — Acquisition-Ready Package
           CIM → P&L → Demo Video → Transition Plan → Data Room
           
Week 6-8:  PHASE 5 — List & Sell
           Acquire Listing → Screen Buyers → Negotiate → Escrow → Close
```

> **Note:** Phases 2 and 3 overlap. You can build missing squads while simultaneously onboarding customers.

---

## EFFORT BUDGET

| Phase | Total Hours | Critical Path Hours | Can Delegate? |
|---|---|---|---|
| Phase 1: Ship It Live | ~8h | ~5h | Partial (domain, GA4) |
| Phase 2: Monetize It | ~25h | ~12h | Partial (landing page, emails) |
| Phase 3: Complete Product | ~30h | ~15h | Yes — agent creation is templatable |
| Phase 4: Acquisition Package | ~20h | ~8h | Partial (CIM, architecture docs) |
| Phase 5: List & Sell | ~5h + ongoing | ~3h | No — founder must lead negotiations |
| **TOTAL** | **~88h** | **~43h** | |

At 2-3 hours/day (solo dev pace), this is roughly **6-8 weeks** of focused execution.

---

## RISK MATRIX

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Acquire rejects pre-revenue listing | High | Critical | Get 3+ paying customers before listing |
| No buyer interest after listing | Medium | High | Record demo video, price competitively, connect all metrics |
| Buyer finds technical debt during DD | Medium | Medium | Remove all TODOs/stubs in Phase 3 |
| Founder dependency scares buyers | High | High | Document everything — SOPs, runbooks, transition plan |
| Revenue drops during sale process | Low | High | Don't neglect the product while selling |
| Stripe account can't transfer | Medium | Critical | Use Stripe's "account transfer" feature — set up early |
| Domain/infrastructure transfer issues | Low | Medium | Document all access credentials clearly |

---

## DAILY PRIORITY FRAMEWORK

When you sit down to work each day, follow this priority order:

1. **Revenue activities first** — Customer outreach, support, onboarding. Revenue is the #1 valuation driver.
2. **Product completeness second** — Fill gaps, remove stubs, add missing agents.
3. **Documentation third** — CIM, runbooks, architecture docs.
4. **Listing prep last** — Acquire.com listing, data room, videos.

> **Never skip #1.** A fully documented product with $0 MRR sells for $7,500. A scrappily documented product with $2,000 MRR sells for $120,000+. Revenue always wins.

---

## SUCCESS METRICS BY PHASE

| Phase | Key Metric | Target |
|---|---|---|
| Phase 1 | Live HTTPS URL | `https://ghostagency.ai` returns 200 |
| Phase 1 | GA4 active | Real-time data visible |
| Phase 2 | MRR | ≥ $297 (3 customers × $97) |
| Phase 2 | Paying customers | ≥ 3 |
| Phase 3 | Agent count | ≥ 12 (1 per squad minimum) |
| Phase 3 | Test pass rate | 100% (zero failures) |
| Phase 3 | TODO count | 0 in production code |
| Phase 4 | CIM completed | Yes |
| Phase 4 | Demo video recorded | Yes |
| Phase 4 | Data room populated | All 10 documents |
| Phase 5 | Listing live | Yes |
| Phase 5 | Buyer inquiries | ≥ 25 (Acquire average) |
| Phase 5 | LOIs received | ≥ 2 |
| Phase 5 | Deal closed | Escrow complete |

---

*This roadmap is your execution plan. Check off items as you complete them. Every checkbox closed brings you closer to a successful exit.*
