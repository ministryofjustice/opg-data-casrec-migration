def get_joins():
    casrec_joins = []
    with open(file_path_validation_mapping, "r") as definition_json:
        def_dict = json.load(definition_json)
        for field, details in def_dict.items():
            if len(details["casrec"]["joins"]) > 0:
                for join in details["casrec"]["joins"]:
                    casrec_joins.append(str(join).strip())

    unique_joins = set(sorted(casrec_joins))

    for join in unique_joins:
        print(join.split(" ON ")[1])

    return unique_joins


def left_join_sql():
    sql = """
    select distinct casrec_csv.pat."Case", casrec_csv.order."Order No", casrec_csv.deputyship."Deputy No"
    from casrec_csv.pat
    inner join casrec_csv.order ON casrec_csv.pat."Case" = casrec_csv.order."Case"
    inner join casrec_csv.deputyship ON casrec_csv.order."Order No" = casrec_csv.deputyship."Order No"
    inner join casrec_csv.deputy ON casrec_csv.deputyship."Deputy No" = casrec_csv.deputy."Deputy No"
    inner join casrec_csv.deputy_remarks ON casrec_csv.deputyship."Deputy No" = casrec_csv.deputy_remarks."Deputy No"
    inner join casrec_csv.remarks ON casrec_csv.pat."Case" = casrec_csv.remarks."Case"
    inner join casrec_csv.sup_activity ON casrec_csv.pat."Case" = casrec_csv.sup_activity."Case"
    inner join casrec_csv.repvis ON casrec_csv.pat."Case" = casrec_csv.repvis."Case"
    """
    return sql
