from receipt_scanner import scan
from receipt_scanner.image.errors import NoContourFoundError
from sqlalchemy.orm import Session

import split.crud.items as items_crud
from split.errors import NoRelevantItemsFoundError
from split.models import Bill
from split.schemas.item import ItemCreateSchema
from split.services.receipt_parser import extract_relevant_information


def generate_items_task(db: Session, bill: Bill) -> None:
    if bill.item_generation is None:
        return
    bill.item_generation.running = False
    bill.item_generation.image_found = False
    bill.item_generation.borders_detected = False
    bill.item_generation.generation_successful = False
    if bill.image is not None:
        try:
            bill.item_generation.image_found = True
            bill.item_generation.borders_detected = True
            scanned_text = scan(image_location=bill.image)
            bill.item_generation.generated_text_lines_raw = scanned_text
            extracted = extract_relevant_information(scanned_text)
            items = [
                items_crud.create(db, ItemCreateSchema(**item, position=index))
                for index, item in enumerate(extracted)
            ]
            bill.items = items
            bill.item_generation.generation_successful = True
        except FileNotFoundError:
            bill.item_generation.image_found = False
            bill.item_generation.borders_detected = False
        except NoContourFoundError:
            bill.item_generation.borders_detected = False
        except NoRelevantItemsFoundError:
            ...
    db.commit()
