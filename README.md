# Python デコレータ チュートリアル

[English README](README.en.md)

Python デコレータを「なぜ必要か」から「型安全な実践的活用」まで段階的に学べるサンプルプロジェクトです。

## 前提条件

- [uv](https://docs.astral.sh/uv/) がインストールされていること

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## セットアップ

```bash
git clone git@github.com:egg-seed/python-decorator-tutorial.git
cd python-decorator-tutorial
uv sync          # 仮想環境の作成 + 依存関係のインストール（1コマンドで完了）
```

## 学習ガイド

各ファイルを番号順に読み進めることで、デコレータの概念を段階的に習得できます。

| ファイル | 対象レベル | 学べること |
|---------|-----------|-----------|
| `01_problem_without_decorator.py` | 入門 | デコレータなしの DRY 違反（なぜ必要か） |
| `02_basic_decorator.py` | 入門 | デコレータの正体・`Callable` 型の基本 |
| `03_decorator_with_args.py` | 入門 | 引数を取るデコレータ（3 重ネスト構造） |
| `04_functools_wraps.py` | 入門 | `functools.wraps` でメタデータを保持 |
| `05_builtin_decorators.py` | 中級 | 組み込み: `@property` / `@classmethod` / `@staticmethod` / `@lru_cache` |
| `06_class_decorator.py` | 中級 | クラスベースデコレータ・状態管理・`Protocol` |
| `07_paramspec_basics.py` | 上級 | `ParamSpec` + `TypeVar` で型安全なデコレータ |
| `08_generic_decorator.py` | 上級 | `Concatenate` で引数を自動注入するパターン |
| `09_decorator_factory.py` | 上級 | 引数あり / なし両対応のファクトリ（`@overload`） |
| `10_stacking_decorators.py` | 上級 | デコレータのスタック順序と型の伝播 |
| `11_real_world_patterns.py` | 上級 | 実務パターン: timer / retry / cache / validate |

## ファイルの実行

```bash
# 任意のファイルを単体実行
uv run python src/decorator_tutorial/01_problem_without_decorator.py
uv run python src/decorator_tutorial/11_real_world_patterns.py
```

## 開発コマンド

```bash
# リント
uv run ruff check .

# リント（自動修正）
uv run ruff check --fix .

# フォーマット
uv run ruff format .

# 型チェック
uv run mypy src/

# テスト
uv run pytest tests/ -v

# カバレッジ付きテスト
uv run pytest tests/ -v --cov=decorator_tutorial --cov-report=term-missing

# 全チェック一括
uv run ruff check . && uv run ruff format --check . && uv run mypy src/ && uv run pytest tests/
```

## Python 3.14 の新機能について

このプロジェクトは Python **3.14** を使用しています。

- **PEP 649 (Deferred Evaluation of Annotations)**: アノテーションの遅延評価がデフォルトになりました。`from __future__ import annotations` は不要です。全ファイルで使用していません。
- **`typing.TypeIs` (PEP 742)**: 型ガードのための `TypeIs` が標準ライブラリに含まれました。

## 型アノテーションの段階的な複雑化

| ファイル | 型レベル | 使用する型要素 |
|---------|---------|--------------|
| 01 | 最小限 | `int`, `str`, `float` |
| 02〜04 | 基本 | `Callable[..., Any]`, `functools.wraps` |
| 05〜06 | 中間 | `type[Self]`, `Protocol`, `__call__` |
| 07〜11 | 厳密 | `ParamSpec`, `TypeVar`, `Concatenate`, `@overload` |
