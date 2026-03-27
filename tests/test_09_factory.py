"""09_decorator_factory のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.09_decorator_factory"
)


def test_unstable_no_args_succeeds_eventually() -> None:
    """引数なし @retry は最終的に成功する。"""
    _mod._call_no_args = 0
    result = _mod.unstable_no_args()
    assert result == "成功（引数なし版）"


def test_unstable_with_args_succeeds_eventually() -> None:
    """引数あり @retry(max_attempts=5) は最終的に成功する。"""
    _mod._call_with_args = 0
    result = _mod.unstable_with_args()
    assert result == "成功（引数あり版）"


def test_retry_no_args_preserves_name() -> None:
    """引数なし @retry はデコレート後も __name__ を保持する。"""
    assert _mod.unstable_no_args.__name__ == "unstable_no_args"


def test_retry_with_args_preserves_name() -> None:
    """引数あり @retry はデコレート後も __name__ を保持する。"""
    assert _mod.unstable_with_args.__name__ == "unstable_with_args"


def test_retry_logs_failures(capsys: pytest.CaptureFixture[str]) -> None:
    """@retry は失敗時にリトライログを出力する。"""
    _mod._call_no_args = 0
    _mod.unstable_no_args()
    captured = capsys.readouterr()
    assert "[RETRY]" in captured.out


def test_retry_raises_after_all_failures() -> None:
    """指定回数すべて失敗した場合は RuntimeError を送出する。"""

    def always_fail() -> None:
        raise ValueError("常に失敗")

    retry = _mod.retry  # importlib 経由で取得

    wrapped = retry(max_attempts=2)(always_fail)
    with pytest.raises(RuntimeError, match="2 回すべて失敗"):
        wrapped()
