"""11: 実務で使うデコレータ 4 パターン。

このファイルで学ぶこと:
- @timer  : 実行時間計測（警告閾値付き）
- @retry  : 自動リトライ（指数バックオフ対応）
- @cache  : シンプルなメモ化キャッシュ（lru_cache の自作）
- @validate: 引数の型・値域を自動検証

すべて ParamSpec + TypeVar で型安全に実装してある。

Python バージョン: 3.14
"""

import functools
import random
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

random.seed(42)  # テストの再現性のためシード固定

P = ParamSpec("P")
T = TypeVar("T")


# --------------------------------------------------------------------------
# ① @timer: 実行時間計測（警告閾値付き）
# --------------------------------------------------------------------------


def timer(threshold_sec: float = 0.0) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """実行時間を計測し、閾値超過時に警告を出すデコレータファクトリ。

    Args:
        threshold_sec: この秒数を超えた場合に [SLOW] 警告を出す（0 で常に表示）
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed >= threshold_sec:
                label = "[SLOW]" if threshold_sec > 0 else "[TIMER]"
                print(f"  {label} {func.__name__}: {elapsed:.4f}秒")
            return result

        return wrapper

    return decorator


# --------------------------------------------------------------------------
# ② @retry: 自動リトライ（指数バックオフ + 対象例外指定）
# --------------------------------------------------------------------------


def retry(
    max_attempts: int = 3,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    backoff: float = 0.0,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """失敗時に自動リトライするデコレータファクトリ。

    Args:
        max_attempts: 最大試行回数
        exceptions: リトライ対象の例外タプル
        backoff: リトライ間隔（秒）。0 の場合は待機なし
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    print(
                        f"  [RETRY] {func.__name__}: "
                        f"{attempt}/{max_attempts} 回目 失敗 ({exc})"
                    )
                    if attempt < max_attempts and backoff > 0:
                        time.sleep(backoff)
            raise RuntimeError(
                f"{func.__name__} が {max_attempts} 回すべて失敗しました"
            ) from last_exc

        return wrapper

    return decorator


# --------------------------------------------------------------------------
# ③ @cache: シンプルなメモ化（lru_cache の自作）
# --------------------------------------------------------------------------


def cache(
    maxsize: int = 128,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """シンプルな LRU キャッシュデコレータファクトリ。

    functools.lru_cache の簡易版。辞書で結果をキャッシュし、
    maxsize を超えた場合は最も古いエントリを削除する。

    Args:
        maxsize: キャッシュするエントリの最大数
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        _cache: dict[tuple[object, ...], T] = {}

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # kwargs をソートしてキーを安定させる
            key = (args, tuple(sorted((kwargs or {}).items())))
            if key in _cache:
                print(f"  [CACHE] {func.__name__}: キャッシュヒット key={key[0]}")
                return _cache[key]
            result = func(*args, **kwargs)
            if len(_cache) >= maxsize:
                # 最も古いエントリを 1 つ削除（Python 3.7+ で dict は挿入順を保持）
                oldest_key = next(iter(_cache))
                del _cache[oldest_key]
            _cache[key] = result
            print(f"  [CACHE] {func.__name__}: 計算して格納 key={key[0]}")
            return result

        return wrapper

    return decorator


# --------------------------------------------------------------------------
# ④ @validate: 引数の型と値域を検証
# --------------------------------------------------------------------------


def validate(**rules: object) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """キーワード引数で型・値域ルールを指定するバリデーションデコレータ。

    Args:
        **rules: 引数名 → (型, min, max) または 型 のルール定義

    例:
        @validate(price=(float, 0, None), quantity=(int, 1, 100))
        def order(price: float, quantity: int) -> str: ...
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            import inspect

            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for param_name, rule in rules.items():
                if param_name not in bound.arguments:
                    continue
                value = bound.arguments[param_name]

                # rule が (型, min, max) のタプルか、型そのものかを判定
                if isinstance(rule, tuple):
                    expected_type, min_val, max_val = rule
                else:
                    expected_type, min_val, max_val = rule, None, None

                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"引数 '{param_name}' は {expected_type.__name__} 型が必要です "
                        f"(実際: {type(value).__name__})"
                    )
                if min_val is not None and value < min_val:
                    raise ValueError(
                        f"引数 '{param_name}' は {min_val} 以上が必要です"
                        f" (実際: {value})"
                    )
                if max_val is not None and value > max_val:
                    raise ValueError(
                        f"引数 '{param_name}' は {max_val} 以下が必要です"
                        f" (実際: {value})"
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator


# --------------------------------------------------------------------------
# 各デコレータの使用例
# --------------------------------------------------------------------------


@timer(threshold_sec=0.01)
def fast_task() -> str:
    """高速なタスク（閾値未満なので SLOW は出ない）。"""
    return "完了"


@timer(threshold_sec=0.01)
def slow_task() -> str:
    """低速なタスク（閾値超過で SLOW 警告が出る）。"""
    time.sleep(0.05)
    return "完了"


_api_call_count = 0


@retry(max_attempts=4, exceptions=(ConnectionError,))
def call_api(endpoint: str) -> dict[str, object]:
    """不安定な API を呼び出すダミー関数。"""
    global _api_call_count
    _api_call_count += 1
    # 最初の 3 回は 70% の確率で失敗（シード固定で再現性あり）
    if _api_call_count <= 3 and random.random() < 0.7:
        raise ConnectionError("タイムアウト")
    return {"status": "ok", "endpoint": endpoint}


@cache(maxsize=4)
def expensive_calc(n: int) -> int:
    """高コストな計算（キャッシュにより 2 回目以降は即返答）。"""
    return n**3


@validate(price=(float, 0.0, None), quantity=(int, 1, 999))
def create_order(price: float, quantity: int) -> str:
    """注文を作成する（バリデーション付き）。"""
    total = price * quantity
    return f"注文確定: 単価 {price}円 × {quantity}個 = {total}円"


def main() -> None:
    """動作確認用エントリポイント。"""
    print("=" * 55)
    print("実務で使うデコレータ 4 パターン")
    print("=" * 55)

    # ① timer
    print("\n--- ① @timer(threshold_sec=0.01) ---")
    print(f"  fast_task: {fast_task()!r}  ← 閾値未満: 出力なし")
    print(f"  slow_task: {slow_task()!r}  ← 閾値超過: [SLOW] が出た")

    # ② retry
    print("\n--- ② @retry(max_attempts=4) ---")
    try:
        result = call_api("/users")
        print(f"  成功: {result}")
    except RuntimeError as e:
        print(f"  全試行失敗: {e}")

    # ③ cache
    print("\n--- ③ @cache(maxsize=4) ---")
    for n in [5, 3, 5, 7, 3]:
        val = expensive_calc(n)
        print(f"    expensive_calc({n}) = {val}")

    # ④ validate
    print("\n--- ④ @validate ---")
    print(f"  {create_order(1980.0, 3)}")
    try:
        create_order(-100.0, 3)
    except ValueError as e:
        print(f"  ValueError: {e}")
    try:
        create_order(500.0, 1000)
    except ValueError as e:
        print(f"  ValueError: {e}")

    print("\n" + "=" * 55)
    print("【まとめ】実務でよく使う 4 パターン")
    print("  @timer   : パフォーマンス計測・SLA 監視")
    print("  @retry   : ネットワーク・外部 API の堅牢化")
    print("  @cache   : 高コスト計算の最適化")
    print("  @validate: 入力値の防衛的チェック")
    print("=" * 55)


if __name__ == "__main__":
    main()
