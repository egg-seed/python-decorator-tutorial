"""02: 基本的なデコレータ。

このファイルで学ぶこと:
- デコレータの正体 = 「関数を受け取り、新しい関数を返す関数」
- 01 の DRY 違反をデコレータで解決する
- Callable 型の基本的な使い方

Python バージョン: 3.14
"""

from collections.abc import Callable
from typing import Any

# --------------------------------------------------------------------------
# デコレータの定義
# --------------------------------------------------------------------------


def log_decorator(func: Callable) -> Callable:
    """関数呼び出しのログを出力するデコレータ。

    引数:
        func: ラップ対象の関数

    戻り値:
        ログ出力機能を追加した新しい関数
    """

    # wrapper はもとの関数を「包む」新しい関数
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 関数呼び出し前にログを出力
        print(f"[開始] {func.__name__} を呼び出します (引数: {args}, {kwargs})")

        # もとの関数を実行
        result = func(*args, **kwargs)

        # 関数呼び出し後にログを出力
        print(f"[完了] {func.__name__} が終わりました (戻り値: {result!r})")
        return result

    return wrapper


# --------------------------------------------------------------------------
# デコレータの適用方法 ①: 手動で適用（@構文の仕組みを理解するために）
# --------------------------------------------------------------------------


def add(a: int, b: int) -> int:
    """2つの整数を足し算する。"""
    return a + b


def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算する。"""
    return a * b


def greet(name: str) -> str:
    """名前を受け取り挨拶文を返す。"""
    return f"こんにちは、{name}さん！"


# 手動でデコレータを適用する
# add = log_decorator(add) と書くのと @log_decorator は同じ意味！
add = log_decorator(add)
multiply = log_decorator(multiply)
greet = log_decorator(greet)


# --------------------------------------------------------------------------
# デコレータの適用方法 ②: @構文（シンタックスシュガー）← こちらが一般的
# --------------------------------------------------------------------------


@log_decorator
def subtract(a: int, b: int) -> int:
    """2つの整数を引き算する。"""
    return a - b


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("デコレータあり: ログ処理を一箇所に集約")
    print("=" * 55)

    result_add = add(3, 5)
    print(f"  → 結果: {result_add}\n")

    result_mul = multiply(4, 7)
    print(f"  → 結果: {result_mul}\n")

    result_greet = greet("太郎")
    print(f"  → 結果: {result_greet!r}\n")

    result_sub = subtract(10, 3)
    print(f"  → 結果: {result_sub}\n")

    print("=" * 55)
    print("【ポイント】")
    print("  ・ログ処理は log_decorator の中に 1 箇所だけ書いた")
    print("  ・フォーマットを変えたい場合は log_decorator を修正するだけ！")
    print("  ・01 の DRY 違反が解消された")
    print("=" * 55)


if __name__ == "__main__":
    main()
