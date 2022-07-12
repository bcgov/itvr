import pandas as pd
import numpy as np
import psycopg2 as pg
from io import StringIO
import psycopg2.extras as extras
from psycopg2 import OperationalError, errorcodes, errors
import sys
from datetime import datetime
import shortuuid
import argparse

# to run in terminal python3 import_redeemed_rebates.py -H localhost -P 5432 -F "filePath"
# Connect to an existing database
# engine = pg.connect(
#     "dbname='itvr' user='postgres' host='127.0.0.1' port='5432' password='admin@123'"
# )

parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", help="hostname", default="localhost")
parser.add_argument("-P", "--port", help="port", default="5432")
parser.add_argument("-F", "--file", help="Spreadsheet", default="")
parser.add_argument("-U", "--user", help="user", default="postgres")
parser.add_argument("-PW", "--password", help="password", default="postgres")

args = parser.parse_args()

conn_params = {
    "host": args.host,
    "port": args.port,
    "database": "itvr",
    "user": args.user,
    "password": args.password,
}


# Define a connect function for PostgreSQL database server
def connect(conn_params):
    conn = None
    try:
        conn = pg.connect(**conn_params)
        print("Database Connection successful..................")

    except OperationalError as err:
        # passing exception to function
        show_psycopg2_exception(err)
        # set the connection to 'None' in case of error
        conn = None
    return conn


excelfile = args.file
print("now processing: ", excelfile)
df = pd.read_excel(excelfile)

# drop columns aside from drivers license and status
df.drop(
    columns=df.columns.difference(["BCDriverLicenseNo", "Status"]), axis=1, inplace=True
)

# drop rows where drivers license is a string or greater than 8 characters
df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df = df[df["BCDriverLicenseNo"].str.len() <= 8]
df = df[pd.to_numeric(df["BCDriverLicenseNo"], errors="coerce").notnull()]

# convert statuses to uppercase and dropo
df["Status"] = df["Status"].str.upper()
df.drop(df[(df.Status == "Cancelled") | (df.Status == "CANCELLED")].index, inplace=True)
df = df.assign(Status="redeemed")

df.rename(
    columns={"BCDriverLicenseNo": "drivers_licence", "Status": "status"}, inplace=True
)

# drop duplicate drivers licenses
df.drop_duplicates(subset="drivers_licence", keep="first", inplace=True)

timestamp = datetime.now()
df["created"] = timestamp
df["modified"] = timestamp

df["is_legacy"] = True

for idx, row in df.iterrows():
    df.loc[idx, "id"] = shortuuid.ShortUUID().random(length=16)


# Define a function that handles and parses psycopg2 exceptions
def show_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occured
    line_n = traceback.tb_lineno
    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


def single_inserts(conn, df, table):
    for i in df.index:
        cols = ",".join(list(df.columns))
        vals = [df.at[i, col] for col in list(df.columns)]
        query = "INSERT INTO %s(%s) VALUES('%s','%s','%s','%s',%s, '%s')" % (
            table,
            cols,
            vals[0],
            vals[1],
            vals[2],
            vals[3],
            vals[4],
            vals[5],
        )
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
        except (Exception, pg.DatabaseError) as error:
            print("Error:", error)
            show_psycopg2_exception(error)
            conn.rollback()
            cursor.close()
            # return 1
    print("single_inserts() done")


# Connect to the database
conn = connect(conn_params)
conn.autocommit = True

single_inserts(conn, df, "go_electric_rebate_application")
