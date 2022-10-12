from pydantic import UUID4
from sqlalchemy.orm import Session

from split.models import Participant
from split.schemas.participant import ParticipantCreateSchema


def get_all_by_bill_id(db: Session, bill_id: UUID4) -> list[Participant]:
    return list(db.query(Participant).filter(Participant.bill_id == bill_id))


def create(db: Session, participant_schema: ParticipantCreateSchema) -> Participant:
    participant = Participant(**participant_schema.dict())
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant
