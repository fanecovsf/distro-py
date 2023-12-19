import importlib
import os


def import_function(module=None, function=None):
    try:
        module_path = os.path.abspath(os.path.join('..', 'modules', module + '.py'))

        loader = importlib.machinery.SourceFileLoader(module, module_path)
        spec = importlib.util.spec_from_loader(loader.name, loader)

        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)

        func = getattr(module, function)
    except Exception as e:
        print(e)
        return None

    return func
