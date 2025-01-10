import inspect


def not_implemented(self_obj: object):
    currentframe = inspect.currentframe()
    name = "(unknown)"
    if currentframe is not None and currentframe.f_back:
        name = currentframe.f_back.f_code.co_name
    return NotImplementedError(f"Metric Type: {type(self_obj)} should implement {name}()")
