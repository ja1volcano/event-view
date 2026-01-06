# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import text

PST = ZoneInfo("America/Los_Angeles")
ROW_LIMIT = 5000


def strip_dict_strs(d):
    stripped = {}
    for k, v in d.items():
        if isinstance(v, str):
            stripped[k] = v.strip()
        else:
            stripped[k] = v
    return stripped


def parse_flexible_datetime(date_string):
    """
    Parses a datetime string that may or may not include hours, minutes, or seconds.
    Attempts to parse with various formats, from most detailed to least.
    """
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%Y-%m-%d %H",
        "%m/%d/%Y %H",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    raise ValueError(f"Unable to parse datetime string: {date_string}")


def parse_query_date(arg):
    if str(arg).split(".", maxsplit=1)[0].isnumeric():
        try:
            return datetime.now(tz=PST) - timedelta(days=abs(int(arg)))
        except ValueError:
            return None
    try:
        return parse_flexible_datetime(arg)
    except ValueError:
        return None


def get_lut(table_name, key_col, val_cols, engine):
    if isinstance(val_cols, str):
        val_cols = [val_cols]
    with engine.connect() as connection:
        sql = f"SELECT {key_col}, {', '.join(val_cols)} FROM dbo.{table_name}"
        print(f"->   Getting data from {table_name}")
        results = connection.execute(text(sql))
        return {
            getattr(_, key_col): {col: getattr(_, col) for col in val_cols}
            for _ in results.all()
            if _ is not None
        }


def flatten_lut(key_name, lut):
    flat_list = []
    for key, value_dict in lut.items():
        flat_dict = {key_name: key}
        flat_dict.update(value_dict)
        flat_list.append(flat_dict)
    return flat_list


def strip_sql(sql):
    return sql.strip().replace("\n", "").replace("    ", " ")


def get_filter_sql(arg, col_name):
    if arg:
        return f" AND {col_name} = {arg}"
    return ""


def parse_response(results):
    data = results.fetchall()
    n = len(data)
    return {
        "meta": {
            "limit": ROW_LIMIT,
            "returned": n,
            "complete": n < ROW_LIMIT,
        },
        "data": data,
    }
