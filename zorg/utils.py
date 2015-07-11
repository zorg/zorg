import importlib


def import_class(module_path):
    module_parts = module_path.split(".")
    module_path = ".".join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])
