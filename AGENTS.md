# Agent Guidelines

These guidelines apply to automated coding agents working in this repository.

## API Conventions

- Prefer one obvious implementation path over configurable abstractions.
- Keep route handlers deterministic and free of network calls.
- Return consistent JSON shapes for both success and error responses.
- Use standard HTTP status codes; avoid encoding status in response bodies.
- Keep seeded demo data small and easy to understand.

## Dependencies

- Add a dependency only when the standard library or existing stack is clearly insufficient.
- Pin new Python dependencies in `requirements.txt`.
- Do not introduce generated lockfiles unless the project starts using that workflow.

## Verification

- Run `python -m py_compile app/main.py` after Python changes.
- Smoke test changed public endpoints with `curl` or an equivalent direct request.
- Document any verification that could not be run.

## Git Hygiene

- Keep commits focused on one intent.
- Do not commit virtualenvs, caches, local config, or machine-specific files.
- Leave unrelated branches and user changes untouched.
