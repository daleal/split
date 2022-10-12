from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.bills as bills_crud
import split.crud.participants as participants_crud
from split import deps
from split.schemas.participant import ParticipantCreateSchema, ParticipantResponseSchema

router = APIRouter()


@router.get("", response_model=list[ParticipantResponseSchema])
def get_all_items_from_bill(
    bill_id: UUID4, db: Session = Depends(deps.get_db),
) -> list[ParticipantResponseSchema]:
    participants = participants_crud.get_all_by_bill_id(db, bill_id)
    return list(participants)


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
