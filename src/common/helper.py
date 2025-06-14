import importlib
import random
import string

from sqlalchemy import inspect


def import_from_string(full_path):
    module_name, class_name = full_path.rsplit(
        ".", 1
    )  # Split module and class
    module = importlib.import_module(module_name)  # Import module
    return getattr(module, class_name)  # Get class from module


def get_index_elements(model):
    primary_keys = [column.name for column in model.__table__.primary_key]
    return primary_keys


def to_dict(model):
    return {
        c.key: getattr(model, c.key)
        for c in inspect(model).mapper.column_attrs
    }


def get_random_str(length: int = 6):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def get_limit_offset(page: int, page_size: int):
    limit = page_size * page
    offset = (page - 1) * page_size
    return limit, offset
