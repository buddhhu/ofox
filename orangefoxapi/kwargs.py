import enum


def build_kwargs(kwargs) -> dict:
    result = {}

    for item in kwargs.items():
        name = item[0]
        data = item[1]

        if name == 'id':
            name = '_id'

        if isinstance(data, enum.Enum):
            data = data.value

        if data or data is False:
            result[name] = data

    return result
