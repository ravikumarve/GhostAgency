from pathlib import Path
from typing import List

from ghostagency.core.exceptions import KnowledgeBaseError


def load_knowledge_base_file(file_path: str) -> str:
    """Load and return content from a single knowledge base file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        raise KnowledgeBaseError(f"Failed to load knowledge base file {file_path}: {e}")


def load_knowledge_base_dir(directory_path: str) -> str:
    """Load and concatenate content from all text files in directory."""
    try:
        kb_dir = Path(directory_path)
        if not kb_dir.exists() or not kb_dir.is_dir():
            raise KnowledgeBaseError(f"Knowledge base directory not found: {directory_path}")

        content_parts = []

        # Support common text file extensions
        text_extensions = {".txt", ".md", ".rst", ".text"}

        for file_path in kb_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in text_extensions:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content_parts.append(f"\n--- {file_path.name} ---\n")
                        content_parts.append(f.read())
                except UnicodeDecodeError:
                    # Skip binary files
                    continue
                except Exception:
                    # Skip files that can't be read
                    continue

        return "\n".join(content_parts)
    except Exception as e:
        raise KnowledgeBaseError(f"Failed to load knowledge base from {directory_path}: {e}")


def chunk_knowledge_base(content: str, max_chunk_size: int = 3000) -> List[str]:
    """Chunk large knowledge base content for LLM context windows."""
    if len(content) <= max_chunk_size:
        return [content]

    chunks = []
    current_chunk = ""

    # Simple chunking by paragraphs
    paragraphs = content.split("\n\n")

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
