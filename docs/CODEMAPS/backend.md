<!-- Generated: 2026-03-27 | Updated: 2026-03-27 (06_class_decorator.py) | Files scanned: 28 | Token estimate: ~650 -->

# Module Reference

> This project has no web backend. This file documents the tutorial module API.

## src/decorator_tutorial/

| File | Key Symbols | Lines (approx) |
|------|-------------|----------------|
| 01_problem_without_decorator.py | `add()`, `multiply()` — DRY-violation demo | ~50 |
| 02_basic_decorator.py | `log_decorator(func)` → wrapper | ~60 |
| 03_decorator_with_args.py | decorator accepting *args/**kwargs | ~60 |
| 04_functools_wraps.py | `@functools.wraps` usage | ~60 |
| 05_builtin_decorators.py | `@property`, `@staticmethod`, `@classmethod` | ~80 |
| 06_class_decorator.py | `CallCounter(__call__, reset)`, `Retry(max_attempts, silent)`, `DecoratorProtocol` | ~156 |
| 07_paramspec_basics.py | `P = ParamSpec("P")`, `T = TypeVar("T")` | ~80 |
| 08_generic_decorator.py | Generic + ParamSpec combined | ~80 |
| 09_decorator_factory.py | `def make_decorator(...) → decorator` | ~80 |
| 10_stacking_decorators.py | `@dec_a @dec_b` application order | ~70 |
| 11_real_world_patterns.py | `@timer`, `@retry`, `@cache`, `@validate` | ~150 |

## Class Decorator Detail (module 06)

```
CallCounter              — stateful decorator class; tracks invocation count
  __init__(func)         → functools.update_wrapper + self.count = 0
  __call__(*args)        → increments count, delegates to self._func
  reset()                → resets count to 0

Retry                    — parameterized class decorator
  __init__(max_attempts, silent)
  __call__(func)         → returns @functools.wraps wrapper with retry loop
    wrapper(*args)       → retries up to max_attempts; raises RuntimeError on exhaustion

DecoratorProtocol        — Protocol defining __call__(func) → Callable interface
```

## Type Annotation Tiers (mypy strictness)

```
Tier 1 (relaxed) : modules 01-04  — disallow_untyped_defs = false
Tier 2 (medium)  : modules 05-06  — disallow_untyped_defs = true, warn_return_any = false
Tier 3 (strict)  : modules 07-11  — full strict mode
```

## Real-World Patterns (module 11)

```
@timer(threshold_ms=100)  → logs warning if execution exceeds threshold
@retry(max_attempts=3, backoff=True) → exponential backoff on exception
@cache                    → dict-based memoization (lru_cache equivalent)
@validate(**rules)        → type + range validation on call arguments
```
