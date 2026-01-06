# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""

from contextlib import contextmanager
from os import getenv, path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

THIS_DIR = path.dirname(path.abspath(__file__))
PACCOUNT = getenv("PACCOUNT").lower()
PASSWORD = getenv("PASSWORD")
HOST = getenv("HOST").lower()
PORT = getenv("PORT").lower()
DBNAME = getenv("DBNAME", "awdb").lower()


def get_conn_str(db=DBNAME, paccount=PACCOUNT, password=PASSWORD, host=HOST, port=PORT):
    driver = "mssql+pymssql"
    if not any((host, port, password, paccount)):
        raise ValueError(
            "A valid user, password, host, & port are required to make a db connection."
        )
    user = rf"EDC\{paccount}"
    return URL.create(
        driver,
        username=user,
        password=password,
        host=host,
        port=port,
        database=db,
    )


def get_awdb_engine(conn_engine=get_conn_str()):
    return create_engine(conn_engine)


@contextmanager
def get_connection_ctx():
    try:
        print(f"-> Creating db connection @ {get_conn_str()}")
        yield get_awdb_engine(get_conn_str())
    finally:
        print("-> Releasing db connection")


if __name__ == "__main__":
    connection_str = get_conn_str()
    print(f"-> Creating db connection @ {connection_str}")
    eng = create_engine(connection_str)
    SQL_STMT = "select * from admin.user_auth where last_nm like 'uriona';"
    try:
        with eng.connect() as connection:
            result = connection.execute(text(SQL_STMT))
            if result.rowcount:
                print("Connection was successful!!")
            else:
                raise (
                    RuntimeError(
                        "'uriona' not in the user table, did he retire? ...he's on a beach I'm sure!"
                    )
                )
    except Exception as err:
        print(f"Connection failed!!! - {err}")
