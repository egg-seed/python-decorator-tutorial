"""06: クラスベースのデコレータ。

このファイルで学ぶこと:
- __call__ を持つクラスをデコレータとして使う方法
- クラスデコレータのメリット: 状態（呼び出し回数など）を保持できる
- Protocol を使ったデコレータの型制約

Python バージョン: 3.14
"""

import functools
from collections.abc import Callable
from typing import Any, Protocol

# --------------------------------------------------------------------------
# パターン①: 呼び出し回数をカウントするデコレータクラス
# --------------------------------------------------------------------------


class CallCounter:
    """関数の呼び出し回数を記録するデコレータクラス。

    クラスにすることで、インスタンス変数 (self.count) に
    状態を持たせることができる。
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        """デコレートする関数を受け取る。"""
        functools.update_wrapper(self, func)  # @wraps 相当の処理
        self._func = func
        self.count = 0  # 呼び出し回数を記録するインスタンス変数

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """関数呼び出し時に実行される。デコレータのラッパー層に相当。"""
        self.count += 1
        print(f"[カウンター] {self._func.__name__} の呼び出し回数: {self.count}回目")
        return self._func(*args, **kwargs)

    def reset(self) -> None:
        """カウンターをリセットする。"""
        self.count = 0


@CallCounter
def process(data: str) -> str:
    """データを処理する（ダミー実装）。"""
    return f"処理済み: {data}"


# --------------------------------------------------------------------------
# パターン②: リトライ機能を持つデコレータクラス（状態管理の応用）
# --------------------------------------------------------------------------


class Retry:
    """失敗時に自動リトライするデコレータクラス。

    max_attempts と delay_seconds を __init__ で設定し、
    __call__ で実際のリトライロジックを実行する。
    """

    def __init__(self, max_attempts: int = 3, silent: bool = False) -> None:
        """リトライ設定を初期化する。

        Args:
            max_attempts: 最大リトライ回数
            silent: True の場合、失敗ログを出力しない
        """
        self.max_attempts = max_attempts
        self.silent = silent

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """デコレートする関数を受け取り、ラップした関数を返す。"""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Exception | None = None
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if not self.silent:
                        print(
                            f"  [リトライ] {func.__name__}: "
                            f"{attempt}/{self.max_attempts} 回目 失敗 ({exc})"
                        )
            raise RuntimeError(
                f"{func.__name__} が {self.max_attempts} 回すべて失敗しました"
            ) from last_exc

        return wrapper


# --------------------------------------------------------------------------
# Protocol: デコレータの型を表現する
# --------------------------------------------------------------------------


class DecoratorProtocol(Protocol):
    """デコレータが満たすべきインターフェースを定義する Protocol。"""

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """関数を受け取り、ラップした関数を返す。"""
        ...


# --------------------------------------------------------------------------
# Retry デコレータの使用例
# --------------------------------------------------------------------------

_attempt_count = 0


@Retry(max_attempts=3)
def unstable_operation() -> str:
    """最初の 2 回は失敗し、3 回目に成功するダミー関数。"""
    global _attempt_count
    _attempt_count += 1
    if _attempt_count < 3:
        raise ConnectionError("接続に失敗しました（ダミーエラー）")
    return "操作成功！"


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("クラスベースのデコレータ")
    print("=" * 55)

    # CallCounter
    print("\n--- CallCounter: 呼び出し回数を記録 ---")
    print(f"  現在のカウント: {process.count}")
    process("データA")
    process("データB")
    process("データC")
    print(f"  合計呼び出し回数: {process.count}")
    process.reset()
    print(f"  リセット後: {process.count}")

    # Retry
    print("\n--- Retry: 自動リトライ ---")
    result = unstable_operation()
    print(f"  結果: {result!r}")

    print("\n" + "=" * 55)
    print("【クラスデコレータのメリット】")
    print("  ・インスタンス変数で状態を管理できる（関数デコレータには難しい）")
    print("  ・__init__ に設定値を持たせてデコレータとしても設定値保持用としても使える")
    print("  ・reset() のような追加メソッドを定義できる")
    print("=" * 55)


if __name__ == "__main__":
    main()
