import pandas as pd
from sqlalchemy import (
    create_engine,
    inspect,
    text,
    select,
    MetaData,
    Table,
)

from utils import clean_903_table, group_calculation, time_difference
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Initialise session variables
filepath = "/workspaces/D2I-Python-Workshops2-2025/Intermediate_Python/Data/903_database.db"

collection_year = 2014
collection_end = datetime(collection_year, 3, 31)

# Read in 903 data from SQL db
engine_903 = create_engine(f"sqlite+pysqlite:///{filepath}")
connection = engine_903.connect()
inspection = inspect(engine_903)

table_names = inspection.get_table_names()

# Uncomment to check database connection
#print(table_names)

metadata_903 = MetaData()

dfs = {}
for table in table_names:
    current_table = Table(table, metadata_903, autoload_with=engine_903)
    with engine_903.connect() as con:
        stmt = select(current_table)
        result = con.execute(stmt).fetchall()
    dfs[table] = pd.DataFrame(result)

# Uncomment to check reading to tables in DF
#print(dfs.keys())
#print(dfs.values())

# Clean all tables in 903
for key, df in dfs.items():
    dfs[key] = clean_903_table(df, collection_end=collection_end)

#uncomment to check data cleaning
#print(dfs['header'])

measures = {}

measures["Header by ethnicity"] = group_calculation(dfs['header'], 'ETHNICITY', 'Header - Ethncities')

measures["Header by age"] = group_calculation(dfs['header'], 'AGE_BUCKETS', 'Header - Age')

dfs["missing"]['MISSING_DURATION'] = time_difference(dfs['missing']['MIS_START_dt'], dfs['missing']['MIS_END_dt'], business_days=True)
print(dfs["missing"])

 