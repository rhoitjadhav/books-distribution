import json
import os

from sqlalchemy.dialects.postgresql import insert

from common.helper import import_from_string, get_index_elements
from database import SessionLocal


def get_fixtures():
    for path, dirnames, filenames in os.walk("tests/fixtures"):
        for filename in filenames:
            file_path = os.path.join(path, filename)
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
