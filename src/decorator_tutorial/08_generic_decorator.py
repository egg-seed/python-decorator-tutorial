"""08: Concatenate で引数を追加・変換するデコレータ。

このファイルで学ぶこと:
- Concatenate: 既存の引数シグネチャに引数を「追加」する型ツール
- ParamSpec だけでは表現できない「引数を注入するデコレータ」のパターン
- 典型的なユースケース: 認証トークン・リクエストオブジェクトの注入

Python バージョン: 3.14
"""

import functools
from collections.abc import Callable
from typing import Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


# --------------------------------------------------------------------------
# Concatenate の基本: 第 1 引数を「追加」する
# --------------------------------------------------------------------------


def inject_user_id(
    func: Callable[Concatenate[str, P], T],
) -> Callable[P, T]:
    """user_id 引数を自動で注入するデコレータ。

    Concatenate[str, P] は「str 型の第 1 引数 + 元の引数シグネチャ P」を表す。
    ラッパーは P の引数だけ受け取り、user_id を自動で付け足して func を呼ぶ。
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # セッション等から取得したユーザー ID を自動で注入
        current_user_id = "user-001"  # 実際はセッションなどから取得
        print(f"  [認証] ユーザー ID を注入: {current_user_id!r}")
        return func(current_user_id, *args, **kwargs)

    return wrapper


@inject_user_id
def get_profile(user_id: str, include_private: bool = False) -> dict[str, object]:
    """ユーザープロフィールを取得する。

    user_id はデコレータが自動で注入するため、呼び出し側は指定不要。
    """
    profile: dict[str, object] = {
        "user_id": user_id,
        "name": "テストユーザー",
    }
    if include_private:
        profile["email"] = "test@example.com"
    return profile


# --------------------------------------------------------------------------
# 実用例: ロガーを注入するデコレータ
# --------------------------------------------------------------------------


class SimpleLogger:
    """シンプルなロガークラス（実用では logging モジュールを使う）。"""

    def __init__(self, name: str) -> None:
        """ロガーを初期化する。"""
        self.name = name

    def info(self, message: str) -> None:
        """INFO レベルのログを出力する。"""
        print(f"  [{self.name}] INFO: {message}")


def inject_logger(
    func: Callable[Concatenate[SimpleLogger, P], T],
) -> Callable[P, T]:
    """SimpleLogger を第 1 引数に自動注入するデコレータ。"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        logger = SimpleLogger(func.__name__)
        return func(logger, *args, **kwargs)

    return wrapper


@inject_logger
def process_order(logger: SimpleLogger, order_id: int, amount: float) -> str:
    """注文を処理する（logger は自動注入）。"""
    logger.info(f"注文 #{order_id} の処理開始 (金額: {amount}円)")
    result = f"注文 #{order_id} 完了"
    logger.info(result)
    return result


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("Concatenate: 引数を自動注入するデコレータ")
    print("=" * 55)

    print("\n--- @inject_user_id: user_id を自動注入 ---")
    # user_id を渡さずに呼び出せる
    profile = get_profile(include_private=True)
    print(f"  プロフィール: {profile}")

    print("\n--- @inject_logger: logger を自動注入 ---")
    # logger を渡さずに呼び出せる
    result = process_order(order_id=42, amount=9800.0)
    print(f"  結果: {result!r}")

    print("\n" + "=" * 55)
    print("【Concatenate の読み方】")
    print("  Callable[Concatenate[str, P], T]")
    print("    → 「str を先頭に持ち、残りが P の引数シグネチャで、T を返す」関数")
    print("  注入されるものの例: user_id, logger, db_session, request など")
    print("=" * 55)


if __name__ == "__main__":
    main()
