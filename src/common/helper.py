import importlib


def import_from_string(full_path):
    module_name, class_name = full_path.rsplit(".", 1)  # Split module and class
    module = importlib.import_module(module_name)  # Import module
    return getattr(module, class_name)  # Get class from module


def get_index_elements(model):
    primary_keys = [
        column.name for column in model.__table__.primary_key
    ]
    return primary_keys
