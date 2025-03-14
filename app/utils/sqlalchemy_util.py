from sqlalchemy.inspection import inspect


def to_dict(model, excludes=[]):
    dict = {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}
    return {k: v for k, v in dict.items() if k not in excludes}
