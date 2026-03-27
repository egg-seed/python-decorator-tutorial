"""08_generic_decorator のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.08_generic_decorator"
)


def test_get_profile_injects_user_id() -> None:
    """inject_user_id は user_id を自動注入してプロフィールを返す。"""
    profile = _mod.get_profile()
    assert profile["user_id"] == "user-001"


def test_get_profile_with_include_private() -> None:
    """include_private=True でプライベート情報も含まれる。"""
    profile = _mod.get_profile(include_private=True)
    assert "email" in profile


def test_get_profile_without_include_private() -> None:
    """include_private=False ではメールが含まれない。"""
    profile = _mod.get_profile(include_private=False)
    assert "email" not in profile


def test_get_profile_logs_injection(capsys: pytest.CaptureFixture[str]) -> None:
    """inject_user_id は注入ログを出力する。"""
    _mod.get_profile()
    captured = capsys.readouterr()
    assert "[認証]" in captured.out
    assert "user-001" in captured.out


def test_process_order_returns_result() -> None:
    """process_order は注文結果を返す。"""
    result = _mod.process_order(order_id=1, amount=5000.0)
    assert "注文 #1 完了" in result


def test_process_order_logs_via_injected_logger(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """inject_logger は SimpleLogger を注入してログを出力する。"""
    _mod.process_order(order_id=99, amount=100.0)
    captured = capsys.readouterr()
    assert "INFO" in captured.out
    assert "99" in captured.out
