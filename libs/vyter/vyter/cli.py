from .import lib


def run():
    factory = lib.create_factory()
    factory.load_rules()
    
