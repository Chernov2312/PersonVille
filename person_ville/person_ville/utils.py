__all__ = ['str_to_bool']


def str_to_bool(value: str) -> bool:
    return value.lower() in {
        'true',
        'yes',
        'on',
        '1',
        'y',
    }
