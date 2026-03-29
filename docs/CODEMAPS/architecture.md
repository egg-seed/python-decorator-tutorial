<!-- Generated: 2026-03-27 | Files scanned: 28 | Token estimate: ~500 -->

# Architecture Overview

## Project Type
Single-package Python tutorial library — no runtime dependencies, dev-only toolchain.

## Structure
```
python-decorator-tutorial/
├── src/decorator_tutorial/   ← 11 progressive tutorial modules + __init__.py
├── tests/                    ← 1:1 test files mirroring each module
├── pyproject.toml            ← uv / ruff / mypy / pytest config
└── uv.lock
```

## Learning Progression
```
01_problem          → motivates decorators (DRY violation)
02_basic            → decorator fundamentals (Callable)
03_decorator_args   → *args/**kwargs in wrapper
04_functools_wraps  → preserving __name__/__doc__
05_builtin          → @property, @staticmethod, @classmethod
06_class_decorator  → __call__-based class decorators
07_paramspec        → ParamSpec + TypeVar (type-safe signatures)
08_generic          → Generic decorators with full type safety
09_factory          → decorator factories (parameterized decorators)
10_stacking         → stacking order and interaction
11_real_world       → timer / retry / cache / validate patterns
```

## Key Design Decisions
- Python 3.14+ required (ParamSpec, strict mypy)
- No runtime dependencies (pure stdlib + typing)
- Each module is self-contained and runnable independently
- mypy strictness relaxed progressively: modules 01-04 allow untyped defs
