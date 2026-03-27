"""10: デコレータの積み重ね（スタック）。

このファイルで学ぶこと:
- 複数のデコレータを重ねたときの適用順序
- 「内側から外側へ」適用され「外側から内側へ」実行される
- 型の伝播: 各デコレータが型を正しく通過させるとスタックしても型安全

Python バージョン: 3.14
"""

import functools
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


# --------------------------------------------------------------------------
# 再利用するデコレータ群（型安全版）
# --------------------------------------------------------------------------


def log(func: Callable[P, T]) -> Callable[P, T]:
    """関数呼び出しをログ出力するデコレータ。"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"  [LOG  ] {func.__name__} 開始")
        result = func(*args, **kwargs)
        print(f"  [LOG  ] {func.__name__} 完了")
        return result

    return wrapper


def timer(func: Callable[P, T]) -> Callable[P, T]:
    """実行時間を計測するデコレータ。"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [TIMER] {func.__name__}: {elapsed:.6f}秒")
        return result

    return wrapper


def validate_positive(func: Callable[P, T]) -> Callable[P, T]:
    """第 1 引数が正の整数であることを検証するデコレータ。"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        first_arg = args[0] if args else None
        if not isinstance(first_arg, int) or first_arg <= 0:
            raise ValueError(f"第 1 引数は正の整数である必要があります: {first_arg!r}")
        print(f"  [VALID] {func.__name__}: 引数 {first_arg} は有効")
        return func(*args, **kwargs)

    return wrapper


# --------------------------------------------------------------------------
# スタックの順序確認
# --------------------------------------------------------------------------
#
# @log
# @timer
# @validate_positive
# def compute(n: int) -> int: ...
#
# ↓ これは以下と同じ
#
# compute = log(timer(validate_positive(compute)))
#
# 適用順序（内から外）: validate_positive → timer → log
# 実行順序（外から内）: log → timer → validate_positive → 元の関数
#                       log → timer → validate_positive → 元の関数（戻り）
#                       log → timer（戻り） → log（戻り）


@log
@timer
@validate_positive
def compute(n: int) -> int:
    """N の 2 乗を計算する（3 つのデコレータをスタック）。"""
    return n * n


# --------------------------------------------------------------------------
# 順序を変えると動作が変わる例
# --------------------------------------------------------------------------


@validate_positive  # ← validate を最外側にすると…
@log
@timer
def compute_v2(n: int) -> int:
    """同じ処理だがデコレータの順序が異なる版。"""
    return n * n


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("デコレータのスタック順序")
    print("=" * 55)

    print("\n--- @log @timer @validate_positive ---")
    print("  (実行順: log → timer → validate → 関数本体)")
    result1 = compute(7)
    print(f"  compute(7) = {result1}\n")

    print("--- エラーの場合（log と timer が先に実行される）---")
    try:
        compute(-1)
    except ValueError as e:
        print(f"  ValueError: {e}")

    print("\n--- @validate_positive @log @timer ---")
    print("  (実行順: validate → log → timer → 関数本体)")
    result2 = compute_v2(5)
    print(f"  compute_v2(5) = {result2}\n")

    print("--- エラーの場合（validate が最初に実行されて即エラー）---")
    try:
        compute_v2(-1)
    except ValueError as e:
        print(f"  ValueError: {e}")

    print("\n" + "=" * 55)
    print("【スタック順序のまとめ】")
    print("  @A        適用: C → B → A（内から外）")
    print("  @B        実行: A → B → C → 本体 → C → B → A")
    print("  @C")
    print("  def func(): ...")
    print()
    print("  ポイント: バリデーションは外側（最後に書く）に置くと")
    print("            無駄な処理（ログ・タイマー）が実行される前にエラーを弾ける")
    print("=" * 55)


if __name__ == "__main__":
    main()
