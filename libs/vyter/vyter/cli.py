from vyter.lib import create_factory


if __name__ == '__main__':
    factory = create_factory()
    factory.load_rules()
    print(factory.rules)
