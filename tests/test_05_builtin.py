"""05_builtin_decorators のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.05_builtin_decorators"
)

Temperature = _mod.Temperature
User = _mod.User
EmailValidator = _mod.EmailValidator
fibonacci = _mod.fibonacci


def test_temperature_celsius_getter() -> None:
    """Celsius property は設定した値を返す。"""
    temp = Temperature(100.0)
    assert temp.celsius == 100.0


def test_temperature_fahrenheit_computed() -> None:
    """Fahrenheit は摂氏から正しく変換される。"""
    temp = Temperature(0.0)
    assert temp.fahrenheit == 32.0
    temp2 = Temperature(100.0)
    assert temp2.fahrenheit == 212.0


def test_temperature_setter_validates() -> None:
    """Celsius setter は絶対零度未満を拒否する。"""
    temp = Temperature(20.0)
    with pytest.raises(ValueError, match="絶対零度"):
        temp.celsius = -300.0


def test_temperature_deleter_resets() -> None:
    """Celsius deleter は温度を 0 にリセットする。"""
    temp = Temperature(50.0)
    del temp.celsius
    assert temp.celsius == 0.0


def test_user_from_dict() -> None:
    """User.from_dict はユーザーを正しく生成する。"""
    user = User.from_dict({"name": "太郎", "email": "taro@example.com", "age": 30})
    assert user.name == "太郎"
    assert user.email == "taro@example.com"
    assert user.age == 30


def test_user_from_json() -> None:
    """User.from_json は JSON 文字列からユーザーを生成する。"""
    user = User.from_json('{"name": "花子", "email": "hanako@example.com", "age": 25}')
    assert user.name == "花子"


def test_email_validator_is_valid() -> None:
    """EmailValidator.is_valid は有効なメールを True と判定する。"""
    assert EmailValidator.is_valid("test@example.com") is True
    assert EmailValidator.is_valid("invalid") is False


def test_email_validator_normalize() -> None:
    """EmailValidator.normalize はトリム・小文字化する。"""
    assert EmailValidator.normalize("  TEST@EXAMPLE.COM  ") == "test@example.com"


def test_fibonacci_correct_values() -> None:
    """Fibonacci は正しいフィボナッチ数を返す。"""
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    assert fibonacci(20) == 6765


def test_fibonacci_cache_works() -> None:
    """2 回目以降の呼び出しはキャッシュが機能する。"""
    fibonacci.cache_clear()
    fibonacci(30)
    info = fibonacci.cache_info()
    # 初回呼び出し後は hits > 0
    fibonacci(30)
    info2 = fibonacci.cache_info()
    assert info2.hits > info.hits
