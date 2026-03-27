"""07: ParamSpec と TypeVar で型安全なデコレータを書く。

このファイルで学ぶこと:
- Callable[..., Any] の問題点（型情報が失われる）
- ParamSpec: 関数の引数シグネチャを型変数として表現する
- TypeVar: 戻り値の型を保持する
- mypy が strict モードでデコレータを正しく解析できるようになる

Python バージョン: 3.14
"""

import functools
import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

# P は「関数の引数シグネチャ」を表す型変数
P = ParamSpec("P")

# T は「関数の戻り値」を表す型変数
T = TypeVar("T")


# --------------------------------------------------------------------------
# 比較①: Callable[..., Any] を使った型なしデコレータ（問題あり）
# --------------------------------------------------------------------------


def log_no_types(func: Callable[..., Any]) -> Callable[..., Any]:
    """型情報を保持しないデコレータ（悪い例）。

    mypy は戻り値を Callable[..., Any] と推論するため、
    デコレートした関数の引数・戻り値の型チェックが効かなくなる。
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[LOG] {func.__name__} 呼び出し")
        return func(*args, **kwargs)

    return wrapper


@log_no_types
def add_untyped(a: int, b: int) -> int:
    """2つの整数を足し算する。"""
    return a + b


# --------------------------------------------------------------------------
# 比較②: ParamSpec + TypeVar を使った型安全デコレータ（良い例）
# --------------------------------------------------------------------------


def log_typed(func: Callable[P, T]) -> Callable[P, T]:
    """型情報を完全に保持するデコレータ（良い例）。

    - P (ParamSpec): func の引数シグネチャをそのまま wrapper に伝える
    - T (TypeVar) : func の戻り値型をそのまま wrapper の戻り値型にする

    これにより mypy は @log_typed を付けても型チェックが正常に動く。
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"[LOG] {func.__name__} 呼び出し")
        return func(*args, **kwargs)

    return wrapper


@log_typed
def add_typed(a: int, b: int) -> int:
    """2つの整数を足し算する。"""
    return a + b


# --------------------------------------------------------------------------
# 実用例: 実行時間計測デコレータ（型安全版）
# --------------------------------------------------------------------------


def timer(func: Callable[P, T]) -> Callable[P, T]:
    """関数の実行時間を計測するデコレータ（型安全版）。"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__}: {elapsed:.6f}秒")
        return result

    return wrapper


@timer
def slow_sum(numbers: list[int]) -> int:
    """リストの合計を計算する（少し時間のかかる処理）。"""
    total = 0
    for n in numbers:
        total += n
    return total


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("ParamSpec + TypeVar による型安全なデコレータ")
    print("=" * 55)

    print("\n--- Callable[..., Any] 版（型情報なし）---")
    # mypy では add_untyped の引数型・戻り値型が Any になる
    result1 = add_untyped(3, 5)
    print(f"  add_untyped(3, 5) = {result1}")

    print("\n--- ParamSpec + TypeVar 版（型安全）---")
    # mypy では add_typed(a: int, b: int) -> int がそのまま保持される
    result2 = add_typed(3, 5)
    print(f"  add_typed(3, 5) = {result2}")

    print("\n--- @timer（型安全な実用デコレータ）---")
    total = slow_sum(list(range(1_000_000)))
    print(f"  合計: {total}")

    print("\n" + "=" * 55)
    print("【ParamSpec のポイント】")
    print("  P = ParamSpec('P')  → 引数シグネチャを型変数として保持")
    print("  T = TypeVar('T')    → 戻り値型を型変数として保持")
    print("  Callable[P, T]      → 元の関数と同じ型シグネチャのデコレータ")
    print("  *args: P.args       → P の位置引数")
    print("  **kwargs: P.kwargs  → P のキーワード引数")
    print("=" * 55)


if __name__ == "__main__":
    main()
