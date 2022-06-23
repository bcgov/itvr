import pandas as pd
import sys
import psycopg2 as pg


# Connect to an existing database
# conn = pg.connect("dbname=itvr user=postgres")
engine = pg.connect(
    "dbname='itvr' user='postgres' host='127.0.0.1' port='5432' password='postgres'"
)

excelfile = sys.argv[1]
print("now processing: ", excelfile)
df = pd.read_excel(excelfile)
# drop columns aside from drivers license and status
df.drop(df.columns.difference(["BCDriverLicenseNo", "Status"]), 1, inplace=True)
# drop rows where drivers license is a string or greater than 8 characters
df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df = df[df["BCDriverLicenseNo"].str.len() <= 8]
df = df[pd.to_numeric(df["BCDriverLicenseNo"], errors="coerce").notnull()]
# convert statuses to uppercase and dropo
df["Status"] = df["Status"].str.upper()
df.drop(df[(df.Status == "Cancelled") | (df.Status == "CANCELLED")].index, inplace=True)
df = df.assign(Status="Redeemed")
print("finished!")
