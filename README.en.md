# Python Decorator Tutorial

[日本語README](README.md)

This sample project helps you learn Python decorators step by step, from why they are needed to type-safe practical usage.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) must be installed

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

```bash
git clone git@github.com:egg-seed/python-decorator-tutorial.git
cd python-decorator-tutorial
uv sync          # Create the virtual environment and install dependencies in one command
```

## Learning Guide

Read the files in numeric order to build your understanding of decorators progressively.

| File | Level | What You Learn |
|------|-------|----------------|
| `01_problem_without_decorator.py` | Beginner | DRY violations without decorators and why decorators matter |
| `02_basic_decorator.py` | Beginner | What decorators really are and the basics of `Callable` typing |
| `03_decorator_with_args.py` | Beginner | Decorators that take arguments and the three-layer nesting structure |
| `04_functools_wraps.py` | Beginner | Preserving metadata with `functools.wraps` |
| `05_builtin_decorators.py` | Intermediate | Built-ins: `@property`, `@classmethod`, `@staticmethod`, and `@lru_cache` |
| `06_class_decorator.py` | Intermediate | Class-based decorators, state management, and `Protocol` |
| `07_paramspec_basics.py` | Advanced | Type-safe decorators with `ParamSpec` and `TypeVar` |
| `08_generic_decorator.py` | Advanced | Injecting arguments with `Concatenate` |
| `09_decorator_factory.py` | Advanced | A decorator factory that supports both with/without arguments via `@overload` |
| `10_stacking_decorators.py` | Advanced | Decorator stacking order and type propagation |
| `11_real_world_patterns.py` | Advanced | Practical patterns: timer, retry, cache, and validate |

## Running Files

```bash
# Run any file independently
uv run python src/decorator_tutorial/01_problem_without_decorator.py
uv run python src/decorator_tutorial/11_real_world_patterns.py
```

## Development Commands

```bash
# Lint
uv run ruff check .

# Lint with auto-fixes
uv run ruff check --fix .

# Format
uv run ruff format .

# Type check
uv run mypy src/

# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ -v --cov=decorator_tutorial --cov-report=term-missing

# Run all checks
uv run ruff check . && uv run ruff format --check . && uv run mypy src/ && uv run pytest tests/
```

## About Python 3.14 Features

This project uses Python 3.14.

- **PEP 649 (Deferred Evaluation of Annotations)**: Deferred evaluation is now the default, so `from __future__ import annotations` is unnecessary and intentionally not used anywhere in this project.
- **`typing.TypeIs` (PEP 742)**: `TypeIs` for type guards is now included in the standard library.

## Gradual Increase in Type Annotation Complexity

| File | Typing Level | Main Typing Features |
|------|--------------|----------------------|
| 01 | Minimal | `int`, `str`, `float` |
| 02-04 | Basic | `Callable[..., Any]`, `functools.wraps` |
| 05-06 | Intermediate | `type[Self]`, `Protocol`, `__call__` |
| 07-11 | Strict | `ParamSpec`, `TypeVar`, `Concatenate`, `@overload` |