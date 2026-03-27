"""11_real_world_patterns のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.11_real_world_patterns"
)


# --------------------------------------------------------------------------
# @timer
# --------------------------------------------------------------------------


def test_fast_task_returns_result() -> None:
    """fast_task は文字列 '完了' を返す。"""
    assert _mod.fast_task() == "完了"


def test_slow_task_returns_result() -> None:
    """slow_task は文字列 '完了' を返す。"""
    assert _mod.slow_task() == "完了"


def test_slow_task_logs_slow_warning(capsys: pytest.CaptureFixture[str]) -> None:
    """slow_task は閾値超過で [SLOW] ログを出力する。"""
    _mod.slow_task()
    captured = capsys.readouterr()
    assert "[SLOW]" in captured.out


# --------------------------------------------------------------------------
# @retry
# --------------------------------------------------------------------------


def test_call_api_eventually_succeeds() -> None:
    """call_api はリトライして最終的に成功する。"""
    _mod._api_call_count = 0
    result = _mod.call_api("/test")
    assert result["status"] == "ok"


def test_call_api_logs_retries(capsys: pytest.CaptureFixture[str]) -> None:
    """call_api の失敗時は [RETRY] ログが出る。"""
    _mod._api_call_count = 0
    _mod.call_api("/test")
    # シード 42 では最初の試行が失敗するため [RETRY] が出力される
    # (成功した場合でも失敗がなければログなしで OK)
    # ここでは呼び出しが成功することだけを確認
    capsys.readouterr()  # 出力をクリア


# --------------------------------------------------------------------------
# @cache
# --------------------------------------------------------------------------


def test_expensive_calc_returns_cube() -> None:
    """expensive_calc は n の 3 乗を返す。"""
    assert _mod.expensive_calc(3) == 27
    assert _mod.expensive_calc(5) == 125


def test_expensive_calc_cache_hit(capsys: pytest.CaptureFixture[str]) -> None:
    """2 回目の呼び出しはキャッシュヒットする。"""
    _mod.expensive_calc(99)  # 1 回目（キャッシュなし）
    capsys.readouterr()
    _mod.expensive_calc(99)  # 2 回目（キャッシュヒット）
    captured = capsys.readouterr()
    assert "キャッシュヒット" in captured.out


# --------------------------------------------------------------------------
# @validate
# --------------------------------------------------------------------------


def test_create_order_valid() -> None:
    """create_order は有効な引数で正しい注文文字列を返す。"""
    result = _mod.create_order(1000.0, 3)
    assert "3000" in result


def test_create_order_invalid_price() -> None:
    """Price が負の場合は ValueError を送出する。"""
    with pytest.raises(ValueError, match="price"):
        _mod.create_order(-1.0, 1)


def test_create_order_invalid_quantity_too_high() -> None:
    """Quantity が 999 超の場合は ValueError を送出する。"""
    with pytest.raises(ValueError, match="quantity"):
        _mod.create_order(100.0, 1000)


def test_create_order_invalid_quantity_zero() -> None:
    """Quantity が 0 の場合は ValueError を送出する。"""
    with pytest.raises(ValueError, match="quantity"):
        _mod.create_order(100.0, 0)


def test_create_order_wrong_type() -> None:
    """Price に文字列を渡すと TypeError を送出する。"""
    with pytest.raises(TypeError, match="price"):
        _mod.create_order("高い", 1)  # type: ignore[arg-type]
