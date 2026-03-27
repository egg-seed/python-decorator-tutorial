"""09: 引数あり / なし両対応のデコレータファクトリ（最終形）。

このファイルで学ぶこと:
- @overload: 引数ありと引数なし両対応の型定義
- 引数なし (@deco) でも引数あり (@deco(n=3)) でも使えるデコレータ
- 実務でよく見るフレームワーク API スタイルの実装

Python バージョン: 3.14
"""

import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar, overload

P = ParamSpec("P")
T = TypeVar("T")


# --------------------------------------------------------------------------
# @overload を使って引数あり/なし両対応のデコレータを定義する
# --------------------------------------------------------------------------
#
# 目標: 以下の 2 つの書き方どちらでも動くデコレータ
#   ① @retry              ← 引数なし（デフォルト値を使う）
#   ② @retry(max_attempts=5)  ← 引数あり
#
# ポイント: 実引数が func (callable) のときと int のときで型が変わるため
#           @overload で 2 パターンの型シグネチャを宣言する。


@overload
def retry(func: Callable[P, T]) -> Callable[P, T]: ...


@overload
def retry(
    *,
    max_attempts: int = ...,
    exceptions: tuple[type[Exception], ...] = ...,
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...


def retry(
    func: Callable[P, T] | None = None,
    *,
    max_attempts: int = 3,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[P, T] | Callable[[Callable[P, T]], Callable[P, T]]:
    """失敗時に自動リトライする型安全なデコレータファクトリ。

    Args:
        func: @retry（引数なし）で使う場合にデコレートする関数が入る
        max_attempts: 最大試行回数（デフォルト 3）
        exceptions: リトライ対象の例外タプル（デフォルト すべての Exception）

    使い方:
        @retry
        def foo(): ...                  # 引数なし

        @retry(max_attempts=5)
        def bar(): ...                  # 引数あり
    """

    def decorator(f: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return f(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    print(
                        f"  [RETRY] {f.__name__}: "
                        f"{attempt}/{max_attempts} 回目 失敗 ({exc})"
                    )
            raise RuntimeError(
                f"{f.__name__} が {max_attempts} 回すべて失敗しました"
            ) from last_exc

        return wrapper

    # 引数なし (@retry) の場合: func に関数が渡されるので直接 decorator を適用
    if func is not None:
        return decorator(func)

    # 引数あり (@retry(...)) の場合: decorator 自体を返す
    return decorator


# --------------------------------------------------------------------------
# 使用例
# --------------------------------------------------------------------------

_call_no_args = 0
_call_with_args = 0


@retry  # 引数なし: デフォルト max_attempts=3
def unstable_no_args() -> str:
    """最初の 2 回は失敗するダミー関数（引数なしデコレータ版）。"""
    global _call_no_args
    _call_no_args += 1
    if _call_no_args < 3:
        raise ValueError("ダミーエラー（引数なし版）")
    return "成功（引数なし版）"


@retry(max_attempts=5, exceptions=(ConnectionError,))  # 引数あり
def unstable_with_args() -> str:
    """最初の 3 回は失敗するダミー関数（引数ありデコレータ版）。"""
    global _call_with_args
    _call_with_args += 1
    if _call_with_args < 4:
        raise ConnectionError("ダミー接続エラー（引数あり版）")
    return "成功（引数あり版）"


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("引数あり/なし両対応 デコレータファクトリ")
    print("=" * 55)

    print("\n--- @retry（引数なし）: max_attempts=3 ---")
    result1 = unstable_no_args()
    print(f"  結果: {result1!r}")

    print("\n--- @retry(max_attempts=5)（引数あり）---")
    result2 = unstable_with_args()
    print(f"  結果: {result2!r}")

    print("\n" + "=" * 55)
    print("【@overload パターンのポイント】")
    print("  ・@overload で型シグネチャを 2 パターン宣言")
    print("  ・実装本体は func=None で両方を受け取れるようにする")
    print("  ・func is not None のとき → 引数なし (@deco)")
    print("  ・func is None のとき     → 引数あり (@deco(...))")
    print("=" * 55)


if __name__ == "__main__":
    main()
