import os


def get_formfile(file):
    file = open(file)
    secret = file.read()
    return secret


def get_env(name):
    if name in os.environ:
        return os.environ[name]
    elif name + "_FILE" in os.environ:
        return get_formfile(os.environ[name + "_FILE"])

    raise Error("Brak Defnincji var")
