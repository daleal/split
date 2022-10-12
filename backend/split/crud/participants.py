from sqlalchemy.orm import Session

from split.models import Participant
from split.schemas.participant import ParticipantCreateSchema


def create(db: Session, participant_schema: ParticipantCreateSchema) -> Participant:
    participant = Participant(**participant_schema.dict())
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant
