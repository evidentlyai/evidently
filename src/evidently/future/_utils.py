import inspect


def not_implemented(self_obj: object):
    return NotImplementedError(
        f"Metric Type: {type(self_obj)} should implement {inspect.currentframe().f_back.f_code.co_name}()"
    )
