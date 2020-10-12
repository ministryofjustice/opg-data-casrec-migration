from sqlalchemy import create_engine
import time


debug_mode = False
db_engine = create_engine(
    "postgresql://casrec:casrec@0.0.0.0:6666/casrecmigration"  # pragma: allowlist secret
)
db_schema = "etl2"


def print_result(df, name):
    print("\n\n==============")
    print(f"{name} final table")
    print("==============")
    print(df.to_markdown())


# def insert_result(df, table_name):
#     t = time.process_time()
#     print("\n\n==============")
#     print(f"inserting {table_name} into database")
#     print("==============")
#     db_engine.execute(f"CREATE SCHEMA IF NOT EXISTS {db_schema};")
#     df.to_sql(
#         name=table_name,
#         con=db_engine,
#         schema=db_schema,
#         if_exists="replace",
#         index=False,
#         method="multi",
#     )
#     get_count = f"select count(*) from {db_schema}.{table_name}"
#     count = db_engine.execute(get_count).fetchall()[0]
#     print(
#         f"inserted {count[0]} records into '{table_name}' table in "
#         f"{round(time.process_time() - t, 2)} "
#         f"seconds"
#     )


def check_table_exists(table_name, schema_name, engine):
    check_exists_statement = f"""
    SELECT EXISTS (
       SELECT FROM information_schema.tables
       WHERE  table_schema = '{schema_name}'
       AND    table_name   = '{table_name}'
    );
    """

    check_exists_result = engine.execute(check_exists_statement)
    for r in check_exists_result:
        table_exists = r.values()[0]

        return table_exists


def create_table_statement(table_name, schema, columns):
    create_statement = f'CREATE TABLE "{schema}"."{table_name}" ('
    for i, col in enumerate(columns):
        create_statement += f'"{col}" text'
        if i + 1 < len(columns):
            create_statement += ","
    create_statement += "); \n\n\n"

    return create_statement


def create_insert_statement(table_name, schema, columns, df):
    insert_statement = f'INSERT INTO "{schema}"."{table_name}" ('
    for i, col in enumerate(columns):
        insert_statement += f'"{col}"'
        if i + 1 < len(columns):
            insert_statement += ","

    insert_statement += ") \n VALUES \n"

    for i, row in enumerate(df.values.tolist()):
        row = [str(x) for x in row]
        row = [
            str(
                x.replace("'", "''")
                .replace("nan", "")
                .replace("&", "")
                .replace(";", "")
                .replace("%", "")
            )
            for x in row
        ]
        row = [f"'{str(x)}'" for x in row]
        single_row = ", ".join(row)

        insert_statement += f"({single_row})"

        if i + 1 < len(df):
            insert_statement += ",\n"
        else:
            insert_statement += ";\n\n\n"
    return insert_statement


def insert_result(df, table_name):
    t = time.process_time()
    print("\n\n==============")
    print(f"inserting {table_name} into database")
    print("==============")
    db_engine.execute(f"CREATE SCHEMA IF NOT EXISTS {db_schema};")

    columns = [x for x in df.columns.values]
    if check_table_exists(table_name, db_schema, db_engine):
        # print(f"Truncating table {db_schema}.{table_name}")
        truncate_statement = f'TRUNCATE TABLE "{db_schema}"."{table_name}"'
        db_engine.execute(truncate_statement)
    else:
        # print(f"Table {db_schema}.{table_name} doesn't exist. Creating table...")
        db_engine.execute(create_table_statement(table_name, db_schema, columns))
        # print(f"Table {db_schema}.{table_name} created")

    db_engine.execute(create_insert_statement(table_name, db_schema, columns, df))

    get_count = f"select count(*) from {db_schema}.{table_name}"
    count = db_engine.execute(get_count).fetchall()[0]
    print(
        f"inserted {count[0]} records into '{table_name}' table in "
        f"{round(time.process_time() - t, 2)} "
        f"seconds"
    )
