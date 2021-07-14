import pandas as pd

from datatypes import mapping

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", -1)


df = pd.read_csv("casrec_dd - main.csv")


table_names = df
table_names["counter"] = (
    table_names["Unnamed: 0"].astype(str).str[:12] == "Logical File"
).cumsum()
table_names_2 = pd.DataFrame()
table_names_2["table_number"] = table_names["counter"]
table_names_2["table_name"] = table_names["Unnamed: 0"].apply(
    lambda x: str(x)[14:] if str(x)[:12] == "Logical File" else "row"
)

table_names_2 = table_names_2.loc[table_names_2.table_name != "row"]

df["counter"] = (df["Unnamed: 0"].astype(str).str[:12] == "Logical File").cumsum()
df.groupby("counter").apply(lambda df: df.iloc[0])
df.rename(columns={"Unnamed: 0": "dd_column_name"}, inplace=True)


datatypes = mapping

map_col_names = {}

for idx, group in df.groupby(df["counter"]):
    # if idx == 1:

    table_name = table_names_2.loc[
        table_names_2["table_number"] == idx, "table_name"
    ].values[0]

    map_col_names[table_name] = {}

    table_df = group[["Column Heading", "Type", "dd_column_name"]].copy()

    for i, row in table_df.iterrows():
        col_name = row[0]
        old_name = row[2]
        # print(f"col_name: {col_name}")
        # print(f"old_name: {old_name}")

        map_col_names[table_name][old_name] = col_name

    table_with_types = pd.merge(
        table_df, mapping, left_on="Type", right_on="code", how="left"
    )

    table_with_types = table_with_types[table_with_types["Column Heading"].notna()]

    # print(table_with_types)
    table_with_types.to_csv(f"./file_per_table/{table_name.lower()}.csv", index=False)
