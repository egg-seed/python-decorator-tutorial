"""03: 引数を取るデコレータ（デコレータファクトリ）。

このファイルで学ぶこと:
- デコレータ自体にパラメータを渡したいときの 3 重ネスト構造
- 「デコレータファクトリ」= デコレータを返す関数
- 各層（ファクトリ → デコレータ → ラッパー）の役割

Python バージョン: 3.14
"""

import time
from collections.abc import Callable
from typing import Any

# --------------------------------------------------------------------------
# パターン①: 繰り返し回数を指定できる @repeat デコレータ
# --------------------------------------------------------------------------


def repeat(times: int) -> Callable:
    """関数を指定回数繰り返すデコレータを生成するファクトリ。

    使い方:
        @repeat(times=3)
        def say_hello() -> None: ...

    ここが「ファクトリ層」: repeat(times=3) を呼ぶと、
    デコレータ本体（下の decorator）が返ってくる。
    """

    # ▼ ここが「デコレータ層」: 関数を受け取って wrapper を返す
    def decorator(func: Callable) -> Callable:
        # ▼ ここが「ラッパー層」: 実際の処理を行う
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result: Any = None
            for i in range(times):
                print(f"  ({i + 1}/{times}回目)")
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


# --------------------------------------------------------------------------
# パターン②: ログレベルを指定できる @log_with_level デコレータ
# --------------------------------------------------------------------------


def log_with_level(level: str = "INFO") -> Callable:
    """ログレベルを指定できるログデコレータを生成するファクトリ。

    Args:
        level: ログレベル文字列（例: "DEBUG", "INFO", "WARNING"）
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"[{level}] {func.__name__} 開始")
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"[{level}] {func.__name__} 完了 ({elapsed:.4f}秒)")
            return result

        return wrapper

    return decorator


# --------------------------------------------------------------------------
# デコレータの適用例
# --------------------------------------------------------------------------


@repeat(times=3)
def say_hello() -> None:
    """挨拶を出力する。"""
    print("    こんにちは！")


@log_with_level(level="DEBUG")
def fetch_data(url: str) -> str:
    """データを取得する（ダミー実装）。"""
    return f"{url} のデータ"


@log_with_level(level="WARNING")
def delete_user(user_id: int) -> bool:
    """ユーザーを削除する（ダミー実装）。"""
    return True


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("引数付きデコレータ（デコレータファクトリ）")
    print("=" * 55)

    print("\n--- @repeat(times=3) ---")
    say_hello()

    print("\n--- @log_with_level(level='DEBUG') ---")
    data = fetch_data("https://example.com/api")
    print(f"  取得結果: {data!r}")

    print("\n--- @log_with_level(level='WARNING') ---")
    success = delete_user(42)
    print(f"  削除結果: {success}")

    print("\n" + "=" * 55)
    print("【3重ネスト構造まとめ】")
    print("  1層目 (ファクトリ): repeat(times=3) ← 引数を受け取る")
    print("  2層目 (デコレータ): decorator(func)  ← 関数を受け取る")
    print("  3層目 (ラッパー):   wrapper(*args)   ← 実際に呼ばれる")
    print("=" * 55)


if __name__ == "__main__":
    main()
