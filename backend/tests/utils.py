from sqlalchemy import inspect


def assert_models_equal(model1, model2, ignore_fields=None):
    if ignore_fields is None:
        ignore_fields = []

    def get_attrs(model):
        mapper = inspect(type(model))
        return {
            col.key: getattr(model, col.key)
            for col in mapper.column_attrs
            if col.key not in ignore_fields
        }

    attrs1 = get_attrs(model1)
    attrs2 = get_attrs(model2)
    assert attrs1 == attrs2, f"Models are not equal: {attrs1} != {attrs2}"