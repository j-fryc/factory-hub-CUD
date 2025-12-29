from typing import Sequence

from fastapi import Depends
from pydantic import ValidationError, BaseModel

from app.cud_services.services_exceptions import DBException
from app.db_sync.exceptions import MQConnectionException, SyncQueueException, MQException
from app.db_sync.mq_producer import (
    MQProducer,
    get_mq_producer,
    MQPublishException
)
from app.models import OutboxEvent, QueueStatus
from app.repositories.repositories_exceptions import DatabaseOperationError
from app.schemas.db_sync_event_schema import OutboxEventDTO
from app.db_sync.sync_repository import SyncRepository, get_sync_repository


class SyncResult(BaseModel):
    total: int
    sent: int
    failed: int
    errors: list[str]


class DBSync:
    MAX_RETRIES = 5

    def __init__(self, mq_producer: MQProducer, repository: SyncRepository):
        self._mq_producer = mq_producer
        self._repository = repository
        self._last_sync_result: SyncResult | None = None

    @property
    def last_sync_result(self) -> SyncResult:
        return self._last_sync_result

    def sync_db(self) -> None:
        with self._mq_producer as mq_producer:
            try:
                data = self._repository.get_unprocessed_events_in_order()
            except DatabaseOperationError as e:
                raise DBException(f"Failed to fetch pending events: {e}")

            return self._process_events(
                events=data,
                mq_producer=mq_producer
            )

    def _process_events(self, events: Sequence[OutboxEvent], mq_producer: MQProducer) -> None:
        self._processed_count = 0
        self._last_sync_result = SyncResult(
            total=0,
            sent=0,
            failed=0,
            errors=[]
        )

        for event in events:
            try:
                event_dto = OutboxEventDTO.model_validate(event)
                message = event_dto.model_dump_json()
            except ValidationError as e:
                self._mark_event(event=event, status=QueueStatus.FAILED)
                self._last_sync_result.failed += 1
                self._last_sync_result.errors.append(f"Event validation failed: {e}")
                raise DBException(f"Event validation failed: {e}") from e
            except Exception as e:
                self._mark_event(event=event, status=QueueStatus.FAILED)
                self._last_sync_result.failed += 1
                self._last_sync_result.errors.append(f"Event serialization failed: {e}")
                raise DBException(f"Event serialization failed: {e}") from e

            try:
                mq_producer.publish_data(
                    msg=message,
                    routing_key=event.aggregate_type
                )
                self._last_sync_result.sent += 1
            except (MQPublishException, MQConnectionException, MQException) as e:
                self._mark_event(event=event, status=QueueStatus.FAILED)
                self._last_sync_result.failed += 1
                self._last_sync_result.errors.append(f"Failed to publish event to queue: {e}")
                raise SyncQueueException(f"Failed to publish event to queue: {e}") from e
            self._mark_event(event=event, status=QueueStatus.SENT)
            self._last_sync_result.total = len(events)

    def _mark_event(self, event: OutboxEvent, status: QueueStatus) -> None:
        try:
            self._repository.mark_event(event=event, status=status)
        except DatabaseOperationError as e:
            raise DBException(f"Database integrity error: {e}") from e


def get_db_synchronizer(
        mq_producer: MQProducer = Depends(get_mq_producer),
        repository: SyncRepository = Depends(get_sync_repository)
) -> DBSync:
    return DBSync(mq_producer=mq_producer, repository=repository)
