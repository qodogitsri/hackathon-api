---
name: code-quality-guidelines
description: Use when editing this FastAPI API repo to keep changes minimal, readable, and contract-aware.
---

# Code Quality Guidelines

## We Expect

- Keep FastAPI endpoints small, typed, and explicit about response models.
- Preserve existing API contracts unless the task intentionally changes them.
- Validate request input with Pydantic models instead of ad hoc checks inside handlers.
- Keep behavior easy to smoke test with `curl` or direct Python checks.
- Update `README.md` when run commands or public endpoints change.

## We Do Not Expect

- Do not add persistence, auth, frameworks, or background services without a direct requirement.
- Do not hide breaking route or response-shape changes.
- Do not swallow errors silently or return ambiguous success responses.
- Do not introduce broad refactors for a narrow endpoint change.
