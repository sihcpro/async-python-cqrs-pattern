def __sif__():
    type_maping = {
        str(str): str,
        str(int): int,
        str(float): float,
        str(dict): dict,
        str(list): list,
    }

    def _type_parse(_type, value):
        type_parse_func = type_maping[str(_type)]
        return type_parse_func(value)

    return _type_parse


type_parse = __sif__()
