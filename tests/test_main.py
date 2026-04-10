from __future__ import annotations

from src.cli.main import configure_windows_stdio_utf8


class _FakeStream:
    def __init__(self):
        self.calls: list[dict[str, str]] = []

    def reconfigure(self, **kwargs):
        self.calls.append(kwargs)


def test_configure_windows_stdio_utf8_reconfigures_standard_streams(monkeypatch):
    stdout = _FakeStream()
    stderr = _FakeStream()

    monkeypatch.setattr("src.cli.main.os.name", "nt")
    monkeypatch.setattr("src.cli.main.sys.stdout", stdout)
    monkeypatch.setattr("src.cli.main.sys.stderr", stderr)

    configure_windows_stdio_utf8()

    assert stdout.calls == [{"encoding": "utf-8"}]
    assert stderr.calls == [{"encoding": "utf-8"}]


def test_configure_windows_stdio_utf8_skips_streams_without_reconfigure(monkeypatch):
    class _NoReconfigure:
        pass

    monkeypatch.setattr("src.cli.main.os.name", "nt")
    monkeypatch.setattr("src.cli.main.sys.stdout", _NoReconfigure())
    monkeypatch.setattr("src.cli.main.sys.stderr", _NoReconfigure())

    configure_windows_stdio_utf8()


def test_configure_windows_stdio_utf8_is_noop_off_windows(monkeypatch):
    stdout = _FakeStream()
    stderr = _FakeStream()

    monkeypatch.setattr("src.cli.main.os.name", "posix")
    monkeypatch.setattr("src.cli.main.sys.stdout", stdout)
    monkeypatch.setattr("src.cli.main.sys.stderr", stderr)

    configure_windows_stdio_utf8()

    assert stdout.calls == []
    assert stderr.calls == []
