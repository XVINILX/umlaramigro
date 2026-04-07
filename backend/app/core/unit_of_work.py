from sqlalchemy.orm import Session


class UnitOfWork:
    """Unit of Work pattern implementation for managing database transactions and connections."""

    def __init__(self, db: Session):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()

    def commit(self):
        """Commit the transaction."""
        try:
            self.db.commit()
        except Exception:
            self.rollback()
            raise

    def rollback(self):
        """Rollback the transaction."""
        self.db.rollback()

    def close(self):
        """Close the database session."""
        self.db.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()
