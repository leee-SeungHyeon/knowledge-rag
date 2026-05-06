from pathlib import Path

import pytest

from app.loader import load_markdown_files


def test_load_markdown_files(tmp_path: Path):
    (tmp_path / "a.md").write_text("# A\nhello", encoding="utf-8")
    (tmp_path / "b.md").write_text("# B\nworld", encoding="utf-8")
    (tmp_path / "ignore.txt").write_text("not markdown", encoding="utf-8")

    docs = load_markdown_files(tmp_path)

    assert len(docs) == 2
    assert {d.source for d in docs} == {"a.md", "b.md"}


def test_load_skips_empty_files(tmp_path: Path):
    (tmp_path / "empty.md").write_text("   \n\n", encoding="utf-8")
    (tmp_path / "real.md").write_text("# Real", encoding="utf-8")

    docs = load_markdown_files(tmp_path)
    assert len(docs) == 1
    assert docs[0].source == "real.md"


def test_load_recursive(tmp_path: Path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "nested.md").write_text("# Nested", encoding="utf-8")

    docs = load_markdown_files(tmp_path)
    assert len(docs) == 1
    assert docs[0].source == "sub/nested.md"


def test_load_uses_relative_path_to_avoid_filename_collision(tmp_path: Path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "note.md").write_text("# A note", encoding="utf-8")
    (tmp_path / "b" / "note.md").write_text("# B note", encoding="utf-8")

    docs = load_markdown_files(tmp_path)

    assert len(docs) == 2
    assert {d.source for d in docs} == {"a/note.md", "b/note.md"}


def test_load_missing_directory_raises():
    with pytest.raises(FileNotFoundError):
        load_markdown_files(Path("/nonexistent/path/zzz"))
