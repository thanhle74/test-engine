from utils.rules.value_range import handle_value_range
from utils.rules.value_template import handle_value_template
from utils.rules.base import handle_default

def build_sql_from_rule(rule_json):
    sub_rules = rule_json["sub_rules"]
    expression = rule_json["expression"]

    conditions = {}
    table_name = None

    for key, rule in sub_rules.items():
        rule_type = rule["type"]
        table_name = rule["db_table"]

        if rule_type == "VALUE_RANGE":
            condition = handle_value_range(rule)
        elif rule_type == "VALUE_TEMPLATE":
            condition = handle_value_template(rule)
        else:
            condition = handle_default(rule)

        conditions[key] = condition

    # Thay thế các RULE_KEY trong biểu thức
    where_clause = expression
    for rule_key, cond in conditions.items():
        where_clause = where_clause.replace(rule_key, f"({cond})")

    sql = f"SELECT * FROM {table_name} WHERE {where_clause};"
    return sql
