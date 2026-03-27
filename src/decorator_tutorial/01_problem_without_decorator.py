"""01: デコレータがないと何が困るか（DRY違反の問題提起）。

このファイルで学ぶこと:
- 同じ処理（ログ出力）を複数の関数にコピペする問題
- 修正が必要になったとき、すべての箇所を書き換えなければならない辛さ
- → この問題を解決するのが「デコレータ」

Python バージョン: 3.14
"""


def add(a: int, b: int) -> int:
    """2つの整数を足し算する。"""
    # ログ処理 ここから -----
    print(f"[開始] add を呼び出します (引数: a={a}, b={b})")
    # ログ処理 ここまで -----

    result = a + b

    # ログ処理 ここから -----
    print(f"[完了] add が終わりました (戻り値: {result})")
    # ログ処理 ここまで -----
    return result


def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算する。"""
    # ログ処理 ここから -----
    # 問題点①: add とまったく同じログ処理をコピペしている
    print(f"[開始] multiply を呼び出します (引数: a={a}, b={b})")
    # ログ処理 ここまで -----

    result = a * b

    # ログ処理 ここから -----
    print(f"[完了] multiply が終わりました (戻り値: {result})")
    # ログ処理 ここまで -----
    return result


def greet(name: str) -> str:
    """名前を受け取り挨拶文を返す。"""
    # ログ処理 ここから -----
    # 問題点②: greet でも同じログ処理が3箇所目として登場している
    print(f"[開始] greet を呼び出します (引数: name={name!r})")
    # ログ処理 ここまで -----

    message = f"こんにちは、{name}さん！"

    # ログ処理 ここから -----
    print(f"[完了] greet が終わりました (戻り値: {message!r})")
    # ログ処理 ここまで -----
    return message


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 50)
    print("デコレータなし: ログ処理を手動でコピペ")
    print("=" * 50)

    result_add = add(3, 5)
    print(f"  → 結果: {result_add}\n")

    result_mul = multiply(4, 7)
    print(f"  → 結果: {result_mul}\n")

    result_greet = greet("太郎")
    print(f"  → 結果: {result_greet!r}\n")

    print("=" * 50)
    print("【問題点まとめ】")
    print("  ・ログ処理が 3 箇所にコピペされている")
    print("  ・ログのフォーマットを変えたい場合、3 箇所すべてを修正する必要がある")
    print("  ・関数が 100 個あれば 100 箇所を修正することになる → DRY 原則違反！")
    print("  ・次のファイル (02_basic_decorator.py) でデコレータによる解決策を学ぼう")
    print("=" * 50)


if __name__ == "__main__":
    main()
