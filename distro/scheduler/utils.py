import importlib
import os

from distro.settings import LOW_QUEUE, HIGH_QUEUE, DEFAULT_QUEUE, MODULES_PATH


def import_function(module=None, function=None):
    try:
        module_path = os.path.join('/app/repo/modules/' + MODULES_PATH, module + '.py')

        loader = importlib.machinery.SourceFileLoader(module, module_path)
        spec = importlib.util.spec_from_loader(loader.name, loader)

        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)

        func = getattr(module, function)
    except Exception as e:
        print(e)
        return None

    return func

def define_queue(name='default'):
    if name == 'default':
        queue = DEFAULT_QUEUE

    if name == 'low':
        queue = LOW_QUEUE

    if name == 'high':
        queue = HIGH_QUEUE

    return queue
