"""05: Python 組み込みデコレータ 4 選。

このファイルで学ぶこと:
- @property  : getter / setter / deleter でカプセル化
- @classmethod: ファクトリメソッドパターン（type[Self]）
- @staticmethod: クラスに属するユーティリティ関数
- @lru_cache : メモ化によるパフォーマンス改善

Python バージョン: 3.14
"""

import functools
import json
from typing import Self

# --------------------------------------------------------------------------
# @property: カプセル化されたプロパティ
# --------------------------------------------------------------------------


class Temperature:
    """摂氏温度を管理するクラス。

    @property を使って、内部の摂氏値を直接触らせずに
    getter / setter / deleter でアクセス制御する。
    """

    def __init__(self, celsius: float) -> None:
        """摂氏温度を初期化する。"""
        # アンダースコアで「直接触らないでね」という慣習
        self._celsius: float = celsius

    @property
    def celsius(self) -> float:
        """摂氏温度を取得する（getter）。"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """摂氏温度をセットする（setter）。-273.15 未満は物理的にありえない。"""
        if value < -273.15:
            raise ValueError(f"絶対零度 (-273.15℃) 未満は設定できません: {value}")
        self._celsius = value

    @celsius.deleter
    def celsius(self) -> None:
        """摂氏温度をリセットする（deleter）。"""
        print("  温度をリセットします")
        self._celsius = 0.0

    @property
    def fahrenheit(self) -> float:
        """華氏温度に変換して返す（計算プロパティ）。"""
        # fahrenheit には setter なし → 読み取り専用
        return self._celsius * 9 / 5 + 32


# --------------------------------------------------------------------------
# @classmethod: ファクトリメソッドパターン
# --------------------------------------------------------------------------


class User:
    """ユーザー情報を管理するクラス。

    @classmethod を使って、複数の入力形式に対応した
    ファクトリメソッドを定義する。
    """

    def __init__(self, name: str, email: str, age: int) -> None:
        """ユーザーを初期化する。"""
        self.name = name
        self.email = email
        self.age = age

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> Self:
        """辞書からユーザーを生成するファクトリメソッド。

        cls を使うことでサブクラスでもそのクラスのインスタンスを返せる。
        """
        return cls(
            name=str(data["name"]),
            email=str(data["email"]),
            age=int(data["age"]),
        )

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """JSON 文字列からユーザーを生成するファクトリメソッド。"""
        data: dict[str, str | int] = json.loads(json_str)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        """開発用の文字列表現。"""
        return f"User(name={self.name!r}, email={self.email!r}, age={self.age})"


# --------------------------------------------------------------------------
# @staticmethod: クラスに属するユーティリティ関数
# --------------------------------------------------------------------------


class EmailValidator:
    """メールアドレスのバリデーションクラス。

    @staticmethod を使って、インスタンスやクラス状態に
    依存しないユーティリティメソッドを定義する。
    """

    @staticmethod
    def is_valid(email: str) -> bool:
        """メールアドレスの形式を簡易チェックする。

        self も cls も不要 → @staticmethod が適切。
        """
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def normalize(email: str) -> str:
        """メールアドレスを小文字・トリムして正規化する。"""
        return email.strip().lower()


# --------------------------------------------------------------------------
# @lru_cache: メモ化（キャッシュ）
# --------------------------------------------------------------------------


@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """N 番目のフィボナッチ数を返す（メモ化あり再帰）。

    @lru_cache がなければ fibonacci(40) は数十億回の再帰呼び出しが発生する。
    キャッシュにより一度計算した値を再利用するため O(n) になる。
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("Python 組み込みデコレータ 4 選")
    print("=" * 55)

    # @property
    print("\n--- @property: Temperature クラス ---")
    temp = Temperature(100.0)
    print(f"  摂氏: {temp.celsius}℃  華氏: {temp.fahrenheit}°F")
    temp.celsius = 0.0
    print(f"  摂氏: {temp.celsius}℃  華氏: {temp.fahrenheit}°F")
    try:
        temp.celsius = -300.0
    except ValueError as e:
        print(f"  エラー: {e}")
    del temp.celsius
    print(f"  リセット後: {temp.celsius}℃")

    # @classmethod
    print("\n--- @classmethod: User ファクトリ ---")
    user1 = User.from_dict({"name": "田中太郎", "email": "taro@example.com", "age": 30})
    user2 = User.from_json(
        '{"name": "山田花子", "email": "hanako@example.com", "age": 25}'
    )
    print(f"  辞書から作成: {user1}")
    print(f"  JSON から作成: {user2}")

    # @staticmethod
    print("\n--- @staticmethod: EmailValidator ---")
    emails = ["Taro@Example.COM ", "invalid-email", "hanako@test.co.jp"]
    for email in emails:
        normalized = EmailValidator.normalize(email)
        valid = EmailValidator.is_valid(normalized)
        print(f"  {email!r:30} → 正規化: {normalized!r:25} 有効: {valid}")

    # @lru_cache
    print("\n--- @lru_cache: フィボナッチ数列 ---")
    for i in [10, 20, 30, 35]:
        result = fibonacci(i)
        info = fibonacci.cache_info()
        print(f"  fibonacci({i:2}) = {result:10}  キャッシュ統計: {info}")

    print("\n" + "=" * 55)
    print("【各デコレータの使いどころ】")
    print("  @property    : 内部実装を隠しつつ属性らしいインターフェースを提供")
    print("  @classmethod : 複数の入力形式に対応したファクトリメソッド")
    print("  @staticmethod: クラスに論理的に属するが状態不要なユーティリティ")
    print("  @lru_cache   : 高コスト計算・再帰関数のパフォーマンス改善")
    print("=" * 55)


if __name__ == "__main__":
    main()
