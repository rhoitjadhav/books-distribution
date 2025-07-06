import json
import os

from sqlalchemy.dialects.postgresql import insert

from common.helper import import_from_string, get_index_elements
from database import SessionLocal


def get_fixtures():
    filenames = [
        "users.json",
        "user_addresses.json",
        "authors.json",
        "publishers.json",
        "books.json",
        "carts.json",
        "cart_items.json",
        "orders.json",
        "order_items.json",
    ]
    for filename in filenames:
        file_path = os.path.join("tests/fixtures", filename)
        with open(file_path, "r") as file:
            yield json.load(file)


def populate_fixtures():
    for fixture in get_fixtures():
        for row in fixture:
            model = import_from_string(row["model"])
            field = row["field"]
            stmt = (
                insert(model)
                .values(**field)
                .on_conflict_do_update(
                    index_elements=get_index_elements(model),
                    set_=field,
                )
            )
            with SessionLocal() as session:
                session.execute(stmt)
                session.commit()
                session.close()


populate_fixtures()
