def handle_value_template(rule):
    column = rule["column"]
    regex = rule["regex"]
    return f"{column} REGEXP '{regex}'"
