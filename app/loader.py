from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    source: str
    content: str


def load_markdown_files(notes_dir: Path) -> list[Document]:
    if not notes_dir.exists():
        raise FileNotFoundError(f"Notes directory not found: {notes_dir}")

    documents: list[Document] = []
    for md_file in sorted(notes_dir.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        if content.strip():
            relative = md_file.relative_to(notes_dir).as_posix()
            documents.append(Document(source=relative, content=content))
    return documents
