"""02.1: 汎用デコレータ（任意のシグネチャに対応）。

このファイルで学ぶこと:
- ParamSpec を使って任意の引数シグネチャを保持する
- TypeVar で戻り値の型を保持する
- functools.wraps で関数メタデータ（__name__ など）を引き継ぐ

Python バージョン: 3.14
"""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def universal_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """任意のシグネチャの関数をラップして、呼び出しログを出す汎用デコレータ。"""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        func_name = func.__name__
        print(f"[汎用ログ] {func_name} を呼び出します")
        print(f"  - 位置引数(args): {args}")
        print(f"  - キーワード引数(kwargs): {kwargs}")

        result = func(*args, **kwargs)

        print(f"[汎用ログ] {func_name} が完了しました (戻り値: {result!r})")
        return result

    return wrapper


@universal_decorator
def no_args() -> str:
    """引数なしの関数"""
    return "OK"


@universal_decorator
def with_positional(a: int, b: int) -> int:
    """位置引数のみの関数"""
    return a + b


@universal_decorator
def with_keyword(name: str, age: int = 20) -> str:
    """キーワード引数を持つ関数"""
    return f"{name} ({age}歳)"


if __name__ == "__main__":
    no_args()
    with_positional(10, 20)
    with_keyword("太郎", age=30)
