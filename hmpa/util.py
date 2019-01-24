def _diff(list_a, list_b):
    diff_a = list(set(list_a).difference(set(list_b)))
    diff_b = list(set(list_b).difference(set(list_a)))
    return diff_a, diff_b
