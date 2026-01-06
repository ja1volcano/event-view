# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""

from flask_restx import Namespace, Resource, reqparse
from sqlalchemy import text

from app import db
from core.utils import (
    ROW_LIMIT,
    get_filter_sql,
    parse_query_date,
    parse_response,
    strip_sql,
)
from models.logs import get_master_model, get_station_model

ns = Namespace("snotelLogs", description="SNOTEL Event Logs")

common_parser = reqparse.RequestParser()
common_parser.add_argument(
    "sDate", type=str, help="YYYY-MM-DD (PST) or integer days back", default="1"
)
common_parser.add_argument(
    "eDate", type=str, help="YYYY-MM-DD (PST) or integer days back", default="0"
)
common_parser.add_argument(
    "eventKey",
    type=int,
    help="filter by event type (sntl_event_key)",
    required=False,
)


stations_parser = reqparse.RequestParser()
for arg in common_parser.args:
    stations_parser.add_argument(arg)
stations_parser.add_argument(
    "stations",
    type=str,
    help="comma delineated list of station IDs to filter on",
    required=False,
)


@ns.route("/stationEvents")
class GetStationEvents(Resource):
    """Gets station event logs items based on query"""

    @ns.marshal_with(get_station_model(ns))
    @ns.expect(stations_parser)
    def get(self):
        """Fetch station events from awdb"""
        args = stations_parser.parse_args()
        start_date = parse_query_date(args["sDate"])
        end_date = parse_query_date(args["eDate"])
        if any(not _ for _ in (start_date, end_date)) or end_date <= start_date:
            ns.abort(400, f"Invalid date arg(s) {args["sDate"]} or {args["eDate"]}")

        try:
            sql_stmt = f"""
                SELECT TOP {ROW_LIMIT} *
                FROM dbo.sntl_event_station_log
                WHERE time_stamp between 
                    '{start_date:%Y-%m-%d %H:%M:%S}' 
                AND 
                    '{end_date:%Y-%m-%d %H:%M:%S}'
                {get_filter_sql(arg=args.stations, col_name="station_id")}
                {get_filter_sql(arg=args.eventKey, col_name="sntl_event_key")}
                ORDER BY time_stamp ASC;
            """
            with db.engine.connect() as connection:
                results = connection.execute(text(strip_sql(sql_stmt)))
                response = parse_response(results=results)
            return response
        except Exception as err:
            ns.abort(500, f"Error executing query: {err}")


master_parser = reqparse.RequestParser()
for arg in common_parser.args:
    master_parser.add_argument(arg)


@ns.route("/masterEvents")
class GetMasterEvents(Resource):
    """Gets master event logs items based on query"""

    @ns.marshal_with(get_master_model(ns))
    @ns.expect(master_parser)
    def get(self):
        """Fetch master events from awdb"""
        args = master_parser.parse_args()
        start_date = parse_query_date(args["sDate"])
        end_date = parse_query_date(args["eDate"])
        if any(not _ for _ in (start_date, end_date)) or end_date <= start_date:
            ns.abort(400, f"Invalid date arg(s) {args["sDate"]} or {args["eDate"]}")
        try:
            sql_stmt = f"""
                SELECT TOP {ROW_LIMIT} *
                FROM dbo.sntl_event_master_log
                WHERE time_stamp between 
                    '{start_date:%Y-%m-%d %H:%M:%S}'
                AND 
                    '{end_date:%Y-%m-%d %H:%M:%S}'
                {get_filter_sql(arg=args.eventKey, col_name="sntl_event_key")}
                ORDER BY time_stamp ASC;
            """
            with db.engine.connect() as connection:
                results = connection.execute(text(strip_sql(sql_stmt)))
                response = parse_response(results=results)
            return response
        except Exception as err:
            ns.abort(500, f"Error executing query: {err}")


system_parser = reqparse.RequestParser()
for arg in common_parser.args:
    system_parser.add_argument(arg)


@ns.route("/systemEvents")
class GetSystemEvents(Resource):
    """Gets system event logs items based on query"""

    @ns.marshal_with(get_station_model(ns))
    @ns.expect(system_parser)
    def get(self):
        """Fetch system events from awdb"""
        args = system_parser.parse_args()
        start_date = parse_query_date(args["sDate"])
        end_date = parse_query_date(args["eDate"])
        if any(not _ for _ in (start_date, end_date)) or end_date <= start_date:
            ns.abort(400, f"Invalid date arg(s) {args["sDate"]} or {args["eDate"]}")
        try:
            sql_stmt = f"""
                SELECT TOP {ROW_LIMIT} *
                FROM dbo.sntl_event_system_log
                WHERE time_stamp between '{start_date:%Y-%m-%d %H:%M:%S}' AND '{end_date:%Y-%m-%d %H:%M:%S}'
                {get_filter_sql(arg=args.eventKey, col_name="sntl_event_key")}
                ORDER BY time_stamp ASC;
            """
            with db.engine.connect() as connection:
                results = connection.execute(text(strip_sql(sql_stmt)))
                response = parse_response(results=results)
            return response
        except Exception as err:
            ns.abort(500, f"Error executing query: {err}")
