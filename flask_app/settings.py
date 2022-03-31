import json


def filter1(arg):
    return arg


def filter2(arg):
    arg["json"] = True
    return json.dumps(arg)


FILTERS_MAP = {"filter1": filter1, "filter2": filter2}
