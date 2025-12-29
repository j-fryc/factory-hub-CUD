from datetime import datetime
from typing import Sequence

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
from sqlmodel import select, Session

from app.db_handler.sync_db_handler import get_sync_db_session
from app.models import OutboxEvent, QueueStatus
from app.repositories.repositories_exceptions import DatabaseOperationError


class SyncRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_unprocessed_events_in_order(self) -> Sequence[OutboxEvent]:
        try:
            return self._db_session.exec(
                select(OutboxEvent)
                .order_by(OutboxEvent.created_at.asc())
                .where(OutboxEvent.status != QueueStatus.SENT)
            ).all()
        except (SQLAlchemyError, OperationalError) as e:
            raise DatabaseOperationError(f"Failed to fetch pending events: {e}")
        except Exception as e:
            raise DatabaseOperationError(f"Unexpected error fetching events: {e}")

    def mark_event(self, event: OutboxEvent, status: QueueStatus):
        try:
            event.status = status
            event.processed_at = datetime.now()
            self._db_session.add(event)
            self._db_session.commit()
        except IntegrityError as e:
            raise DatabaseOperationError(f"Database integrity error: {e}") from e
        except (SQLAlchemyError, OperationalError) as e:
            raise DatabaseOperationError(f"Database error: {e}") from e
        except Exception as e:
            raise DatabaseOperationError(f"Unexpected database error: {e}") from e


def get_sync_repository(db_session: Session = Depends(get_sync_db_session)) -> SyncRepository:
    return SyncRepository(db_session=db_session)
