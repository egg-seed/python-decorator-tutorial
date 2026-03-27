"""04: functools.wraps でメタデータを保持する。

このファイルで学ぶこと:
- デコレータを使うと関数名・docstring が失われる問題
- functools.wraps でメタデータを保持する方法
- なぜデコレータには @wraps が必須なのか

Python バージョン: 3.14
"""

import functools
from collections.abc import Callable
from typing import Any

# --------------------------------------------------------------------------
# 問題: @wraps なしのデコレータ
# --------------------------------------------------------------------------


def log_without_wraps(func: Callable) -> Callable:
    """@wraps を使わないデコレータ（悪い例）。"""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("[LOG] 呼び出し中...")
        return func(*args, **kwargs)

    return wrapper


@log_without_wraps
def add_bad(a: int, b: int) -> int:
    """2つの整数を足し算する（wraps なし版）。"""
    return a + b


# --------------------------------------------------------------------------
# 解決: @wraps ありのデコレータ
# --------------------------------------------------------------------------


def log_with_wraps(func: Callable) -> Callable:
    """@wraps を使うデコレータ（良い例）。"""

    @functools.wraps(func)  # ← これを付けるだけで OK！
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("[LOG] 呼び出し中...")
        return func(*args, **kwargs)

    return wrapper


@log_with_wraps
def add_good(a: int, b: int) -> int:
    """2つの整数を足し算する（wraps あり版）。"""
    return a + b


# --------------------------------------------------------------------------
# @wraps が保持する情報一覧
# --------------------------------------------------------------------------


def show_metadata(func: Callable) -> None:
    """関数のメタデータを表示する。"""
    print(f"  __name__     : {func.__name__}")
    print(f"  __qualname__ : {func.__qualname__}")
    print(f"  __doc__      : {func.__doc__!r}")
    print(f"  __module__   : {func.__module__}")


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("functools.wraps によるメタデータ保持")
    print("=" * 55)

    print("\n--- @wraps なし (悪い例) ---")
    show_metadata(add_bad)
    # __name__ が 'wrapper' になってしまっている！
    # デバッグ時に「どの関数か」分からなくなる

    print("\n--- @wraps あり (良い例) ---")
    show_metadata(add_good)
    # __name__ が 'add_good' のまま保持されている

    print("\n--- 実行結果の比較 ---")
    print(f"  add_bad(3, 5)  = {add_bad(3, 5)}")
    print(f"  add_good(3, 5) = {add_good(3, 5)}")

    print("\n" + "=" * 55)
    print("【ルール】デコレータを書くときは必ず @functools.wraps(func) を付ける")
    print("  理由: ログ・デバッグ・テスト・IDE の補完で正しい情報が見えるようになる")
    print("=" * 55)


if __name__ == "__main__":
    main()
