# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""

from flask_restx import fields

from .static import get_network_lut, get_state_lut

COUNTRY_LOOKUP = get_state_lut()
NETWORK_LOOKUP = get_network_lut()


def get_master_model(ns):
    return ns.model(
        "masterLut",
        {
            "master_id": fields.Integer(readonly=True, description="API row limit"),
            "master_nm": fields.String(
                readonly=True,
                description="number of rows returned for query",
                attribute=lambda x: x.get("master_nm", "").strip(),
            ),
            "description": fields.String(
                readonly=True, description="a description of the master station"
            ),
        },
    )


def get_events_model(ns):
    return ns.model(
        "eventsLut",
        {
            "sntl_event_key": fields.Integer(
                readonly=True, description="event type key"
            ),
            "event_name": fields.String(
                readonly=True, description="short name for event type"
            ),
            "description_of_event": fields.String(
                readonly=True, description="a description of event type"
            ),
        },
    )


def get_meta_model(ns):
    return ns.model(
        "meta",
        {
            "limit": fields.Integer(readonly=True, description="API row limit"),
            "returned": fields.Integer(
                readonly=True, description="number of rows returned for query"
            ),
            "complete": fields.Boolean(
                readonly=True, description="all requested data was returned"
            ),
        },
    )


def get_stations_model(
    ns,
    country_lookup=COUNTRY_LOOKUP,
    network_lookup=NETWORK_LOOKUP,
):
    def lookup_state(cd):
        return country_lookup.get(cd, "UNKNOWN").get("fips_st_cd", "UNKNOWN")

    def lookup_network(cd):
        return network_lookup.get(cd, "UNKNOWN").get("ntwk_cd", "UNKNOWN")

    return ns.model(
        "awdb_sta_lut",
        {
            "ntwk_sta_id": fields.Integer(
                readonly=True,
                description="station key",
            ),
            "awdb_sta_key": fields.Integer(
                readonly=True,
                description="station key",
            ),
            "sta_nm": fields.String(
                readonly=True,
                description="station name",
            ),
            "st_key": fields.String(
                readonly=True,
                description="state code",
                attribute=lambda x: lookup_state(x.get("st_key", "UNKNOWN")),
            ),
            "ntwk_key": fields.String(
                readonly=True,
                description="network code",
                attribute=lambda x: lookup_network(x.get("ntwk_key", "UNKNOWN")),
            ),
            "dco_cd": fields.String(
                readonly=True,
                description="dco code",
            ),
            "tm_zone": fields.Integer(
                readonly=True,
                description="timezone offset",
            ),
            "lat": fields.Float(
                readonly=True,
                description="latitude",
            ),
            "lon": fields.Float(
                readonly=True,
                description="longitude",
            ),
            "elev": fields.Float(
                readonly=True,
                description="elevation",
            ),
            "in_srvc_dt": fields.DateTime(
                readonly=True,
                description="station start date",
            ),
            "out_srvc_dt": fields.DateTime(
                readonly=True,
                description="station end date",
            ),
            "rmk": fields.String(
                readonly=True,
                description="remark",
            ),
            "huc": fields.String(
                readonly=True,
                description="huc",
            ),
        },
    )


def get_iridium_model(ns):
    return ns.model(
        "meta",
        {
            "station_id": fields.Integer(
                readonly=True,
                description="station id",
            ),
            "iridium_imei": fields.String(
                readonly=True,
                description="iridium id",
            ),
            "is_iridium_enabled": fields.Boolean(
                readonly=True,
                description="iridium enabled?",
            ),
            "data_to_group_channel": fields.String(
                readonly=True,
                description="group and channel mapping",
            ),
            "midnight_group": fields.String(
                readonly=True,
                description="midnight only group",
            ),
            "lrgs_message_format_cd": fields.String(
                readonly=True,
                description="message format code",
            ),
            "is_deleted": fields.Boolean(
                readonly=True,
                description="replay data only mode?",
            ),
            "last_updated": fields.DateTime(
                readonly=True,
                description="last updated date",
            ),
            "updated_by": fields.String(
                readonly=True,
                description="updated by",
            ),
        },
    )


def get_goes_model(ns):
    return ns.model(
        "meta",
        {
            "station_id": fields.Integer(
                readonly=True,
                description="station id",
            ),
            "goes_id": fields.String(
                readonly=True,
                description="goes id",
            ),
            "is_goes_enabled": fields.Boolean(
                readonly=True,
                description="goes enabled?",
            ),
            "data_to_group_channel": fields.String(
                readonly=True,
                description="group and channel mapping",
            ),
            "midnight_group": fields.String(
                readonly=True,
                description="midnight only group",
            ),
            "lrgs_message_format_cd": fields.String(
                readonly=True,
                description="message format code",
            ),
            "is_deleted": fields.Boolean(
                readonly=True,
                description="replay data only mode?",
            ),
            "last_updated": fields.DateTime(
                readonly=True,
                description="last updated date",
            ),
            "updated_by": fields.String(
                readonly=True,
                description="updated by",
            ),
        },
    )
