# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""

from flask_restx import Namespace, Resource, reqparse

from core.utils import flatten_lut
from models import event_lut, goes_lut, iridium_lut, master_lut, stations_lut
from models.luts import (
    get_events_model,
    get_goes_model,
    get_iridium_model,
    get_master_model,
    get_stations_model,
)

master_lut_parser = reqparse.RequestParser()
master_lut_parser.add_argument(
    "activeOnly",
    type=lambda _: _.lower().startswith("t"),
    help="only return active master stations",
    default=True,
)

ns = Namespace("lookupTables", description="pertinent look up tables")


@ns.route("/mastersTable")
class GetMasterTable(Resource):
    """Gets master events look up table"""

    @ns.marshal_with(get_master_model(ns))
    @ns.expect(master_lut_parser)
    def get(self):
        """Fetch master lut from awdb"""
        active_only = master_lut_parser.parse_args()["activeOnly"]
        try:
            flat_lut = flatten_lut(key_name="master_id", lut=master_lut)
            if active_only:
                flat_lut[:] = [_ for _ in flat_lut if _["is_active"]]
            return flat_lut
        except Exception as err:
            ns.abort(500, f"Error marshalling table: {err}")


@ns.route("/eventsTable")
class GetEventsTable(Resource):
    """Gets log events look up table"""

    @ns.marshal_with(get_events_model(ns))
    def get(self):
        """Fetch events lut from awdb"""
        try:
            return flatten_lut(key_name="sntl_event_key", lut=event_lut)
        except Exception as err:
            ns.abort(500, f"Error marshalling table: {err}")


@ns.route("/stationsTable")
class GetStationsTable(Resource):
    """Gets stations look up table"""

    @ns.marshal_with(get_stations_model(ns))
    def get(self):
        """Fetch stations lut from awdb"""
        try:

            is_numeric_id = {
                k: v for k, v in stations_lut.items() if k.strip().isnumeric()
            }
            is_active = {
                k: v for k, v in is_numeric_id.items() if v["out_srvc_dt"].year == 2100
            }
            is_telemetered = {
                k: v
                for k, v in is_active.items()
                if v["ntwk_key"] in (5, 9, 14, 15, 17, 18)
            }
            return flatten_lut(key_name="ntwk_sta_id", lut=is_telemetered)
        except Exception as err:
            ns.abort(500, f"Error marshalling table: {err}")


@ns.route("/goesTable")
class GetGoesTable(Resource):
    """Gets goes config look up table"""

    @ns.marshal_with(get_goes_model(ns))
    def get(self):
        """Fetch GOES config lut from awdb"""
        try:
            has_goes_id = {k: v for k, v in goes_lut.items() if v["goes_id"]}
            return flatten_lut(key_name="station_id", lut=has_goes_id)
        except Exception as err:
            ns.abort(500, f"Error marshalling table: {err}")


@ns.route("/iridiumTable")
class GetIridiumTable(Resource):
    """Gets iridium config look up table"""

    @ns.marshal_with(get_iridium_model(ns))
    def get(self):
        """Fetch iridium config lut from awdb"""
        try:
            has_iridium_id = {k: v for k, v in iridium_lut.items() if v["iridium_imei"]}
            return flatten_lut(key_name="station_id", lut=has_iridium_id)
        except Exception as err:
            ns.abort(500, f"Error marshalling table: {err}")
