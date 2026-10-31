import os

from src.paths import normalize


def _fixture(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real)
    return real, link


def test_absolute_unchanged(tmp_path):
    real, link = _fixture(tmp_path)
    p = str(link / "x.txt")
    assert normalize(p) == p


def test_symlink_resolved(tmp_path):
    real, link = _fixture(tmp_path)
    assert normalize(str(link / "x.txt")) == str(real / "x.txt")


def test_relative(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert normalize(os.path.join("a", "b")) == str(tmp_path / "a" / "b")
