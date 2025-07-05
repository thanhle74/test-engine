def handle_value_range(rule):
    column = rule["column"]
    min_val = rule["min"]
    max_val = rule["max"]
    return f"{column} BETWEEN {min_val} AND {max_val}"
