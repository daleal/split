from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.bills as bills_crud
import split.crud.participants as participants_crud
from split import deps
from split.schemas.participant import ParticipantCreateSchema, ParticipantResponseSchema

router = APIRouter()


@router.post("", response_model=ParticipantResponseSchema)
def create_participant(
    bill_id: UUID4,
    participant_schema: ParticipantCreateSchema,
    db: Session = Depends(deps.get_db),
) -> ParticipantResponseSchema:
    bill = bills_crud.get_by_id(db, bill_id)
    participant = participants_crud.create(db, participant_schema)
    bill.participants.append(participant)
    db.commit()
    db.refresh(participant)
    return participant
