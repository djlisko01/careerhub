# Backend

## Notes

### Circular imports in models

SQLAlchemy models use `TYPE_CHECKING` guards to avoid circular imports caused by bidirectional relationships (e.g. `User` ↔ `Address`). Imports inside `if TYPE_CHECKING:` blocks are only evaluated by the type checker — never at runtime. SQLAlchemy resolves the string-based relationship references (e.g. `"Address"`) through its own mapper registry, so the actual class doesn't need to be imported at runtime.

If you'd prefer to avoid this pattern, the alternative is using `backref` instead of `back_populates` so the relationship is only defined on one side. The tradeoff is that `backref` is implicit and less visible to the type checker.
