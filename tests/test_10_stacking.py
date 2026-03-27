"""10_stacking_decorators のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.10_stacking_decorators"
)


def test_compute_returns_square() -> None:
    """Compute は n の 2 乗を返す。"""
    assert _mod.compute(7) == 49
    assert _mod.compute(3) == 9


def test_compute_v2_returns_square() -> None:
    """compute_v2 も n の 2 乗を返す。"""
    assert _mod.compute_v2(5) == 25


def test_compute_raises_on_non_positive() -> None:
    """Compute は非正の引数で ValueError を送出する。"""
    with pytest.raises(ValueError, match="正の整数"):
        _mod.compute(-1)


def test_compute_v2_raises_on_non_positive() -> None:
    """compute_v2 も非正の引数で ValueError を送出する。"""
    with pytest.raises(ValueError, match="正の整数"):
        _mod.compute_v2(0)


def test_compute_logs_all_decorators(capsys: pytest.CaptureFixture[str]) -> None:
    """Compute は log, timer, validate すべてのログが出力される。"""
    _mod.compute(4)
    captured = capsys.readouterr()
    assert "[LOG  ]" in captured.out
    assert "[TIMER]" in captured.out
    assert "[VALID]" in captured.out


def test_compute_preserves_name() -> None:
    """スタックしても __name__ は保持される。"""
    assert _mod.compute.__name__ == "compute"
