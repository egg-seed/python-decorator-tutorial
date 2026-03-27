"""06_class_decorator のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.06_class_decorator"
)


def test_call_counter_initial_count() -> None:
    """CallCounter の初期カウントは 0。"""
    # process は CallCounter でデコレートされているが、モジュール読み込み時に
    # main() は呼ばれないため count = 0 から始まる
    _mod.process.reset()
    assert _mod.process.count == 0


def test_call_counter_increments() -> None:
    """Process を呼ぶたびにカウントが増える。"""
    _mod.process.reset()
    _mod.process("テスト1")
    assert _mod.process.count == 1
    _mod.process("テスト2")
    assert _mod.process.count == 2


def test_call_counter_reset() -> None:
    """reset() はカウントを 0 に戻す。"""
    _mod.process("データ")
    _mod.process.reset()
    assert _mod.process.count == 0


def test_process_returns_correct_result() -> None:
    """Process は正しい処理済み文字列を返す。"""
    result = _mod.process("hello")
    assert result == "処理済み: hello"


def test_retry_succeeds_eventually() -> None:
    """Retry デコレータは最終的に成功する。"""
    # unstable_operation は 3 回目に成功する設計
    # モジュール読み込み後にカウントがリセットされるよう _attempt_count を初期化
    _mod._attempt_count = 0
    result = _mod.unstable_operation()
    assert result == "操作成功！"


def test_retry_logs_failures(capsys: pytest.CaptureFixture[str]) -> None:
    """Retry は失敗のたびにログを出す。"""
    _mod._attempt_count = 0
    _mod.unstable_operation()
    captured = capsys.readouterr()
    assert "[リトライ]" in captured.out
