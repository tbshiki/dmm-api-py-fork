def to_str(val):

    return "" if val is None else str(val)


def _convert_value(pattern, value):
    if pattern["name"] == "str":
        return to_str(value)
    elif pattern["name"] == "dict_list":
        if value is None:
            value_list = []
        else:
            value_list = [to_str(get_dict_value(v, pattern["value"])) for v in value]
        return "[" + ",".join(value_list) + "]"

    raise ValueError(f"Unknown pattern name: {pattern['name']}")


def dict_to_list(d, rule):
    result = []
    for name, (keys, pattern) in rule.items():
        if not keys:
            value = d.get(name)
        else:
            value = get_dict_value(d, keys)

        result.append(_convert_value(pattern, value))

    return result


def get_dict_value(d, keys):
    for key in keys:
        d = d[key]  # Raises KeyError if the key is not found
        if d is None:
            break
    return d
