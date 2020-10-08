from sqlalchemy import create_engine
import time


debug_mode = False
db_engine = create_engine('postgresql://casrec:casrec@0.0.0.0:6666/casrecmigration')
db_schema = "etl2"

def print_result(df, name):
    print("\n\n==============")
    print(f"{name} final table")
    print("==============")
    print(df.to_markdown())

def insert_result(df, table_name):
    t = time.process_time()
    print("\n\n==============")
    print(f"inserting {table_name} into database")
    print("==============")
    db_engine.execute(f"CREATE SCHEMA IF NOT EXISTS {db_schema};")
    df.to_sql(name=table_name,  con=db_engine, schema=db_schema, if_exists='replace',
              index=False, method='multi')
    get_count = f"select count(*) from {db_schema}.{table_name}"
    count = db_engine.execute(get_count).fetchall()[0]
    print(f"inserted records: {table_name}: {count} in "
          f"{round(time.process_time() - t, 2)} "
          f"seconds")
