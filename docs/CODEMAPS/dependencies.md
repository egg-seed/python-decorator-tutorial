<!-- Generated: 2026-03-27 | Files scanned: 28 | Token estimate: ~250 -->

# Dependencies

## Runtime
None — zero production dependencies.

## Dev Dependencies (pyproject.toml)
| Package     | Version  | Purpose                        |
|-------------|----------|--------------------------------|
| pytest      | >=8.3.0  | Test runner                    |
| pytest-cov  | >=6.0.0  | Coverage reporting             |
| mypy        | >=1.15.0 | Static type checking (strict)  |
| ruff        | >=0.11.0 | Linting + formatting           |

## Build
| Package      | Version           | Role          |
|--------------|-------------------|---------------|
| uv_build     | >=0.10.7,<0.11.0  | Build backend |

## stdlib Modules Used Across Tutorials
- `collections.abc.Callable` — function type annotations
- `functools` — `wraps`, `lru_cache`
- `typing` — `ParamSpec`, `TypeVar`, `Any`, `Generic`
- `time` — execution timing (module 11)
- `random` — retry simulation (module 11)
