# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""

from flask_restx import fields

from . import LookupField, event_lut, master_lut


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


def get_master_model(ns):
    master_event = ns.model(
        "masterEvent",
        {
            "time_stamp": fields.DateTime(
                readOnly=True, description="datetime (PST) of the event"
            ),
            "master_id": fields.Integer(readOnly=True, description="master station id"),
            "master_nm": LookupField(
                key="master_id",
                lut=master_lut,
                attr_key="master_nm",
                description="master station name",
            ),
            "sntl_event_key": fields.Integer(readOnly=True, description="event type"),
            "sntl_event_desc": LookupField(
                key="sntl_event_key",
                lut=event_lut,
                attr_key="event_name",
                description="event name",
            ),
            "message": fields.String(readOnly=True, description="event message"),
        },
    )

    return ns.model(
        "masterResponse",
        {
            "data": fields.List(
                fields.Nested(master_event), description="an array of master events"
            ),
            "meta": fields.Nested(
                get_meta_model(ns), description="information about the returned results"
            ),
        },
    )


def get_station_model(ns):
    station_event = ns.model(
        "stationEvent",
        {
            "time_stamp": fields.DateTime(
                readOnly=True, description="datetime (PST) of the event"
            ),
            "sampled": fields.DateTime(
                readOnly=True, description="datetime of the sampled data (PST or local)"
            ),
            "station_id": fields.Integer(readOnly=True, description="station id"),
            "group_id": fields.Integer(readOnly=True, description="group id"),
            "channel": fields.Integer(readOnly=True, description="channel"),
            "sntl_event_key": fields.Integer(readOnly=True, description="event type"),
            "sntl_event_desc": LookupField(
                key="sntl_event_key",
                lut=event_lut,
                attr_key="event_name",
                description="event name",
            ),
            "message": fields.String(
                readOnly=True, description="station event message"
            ),
        },
    )

    return ns.model(
        "stationResponse",
        {
            "data": fields.List(
                fields.Nested(station_event), description="an array of station events"
            ),
            "meta": fields.Nested(
                get_meta_model(ns), description="information about the returned results"
            ),
        },
    )


def get_system_model(ns):
    system_event = ns.model(
        "systemEvent",
        {
            "time_stamp": fields.DateTime(
                readOnly=True, description="datetime (PST) of the event"
            ),
            "sntl_event_key": fields.Integer(readOnly=True, description="event type"),
            "sntl_event_desc": LookupField(
                key="sntl_event_key", lut=event_lut, description="event description"
            ),
            "message": fields.String(readOnly=True, description="system event message"),
        },
    )

    return ns.model(
        "stationResponse",
        {
            "data": fields.List(
                fields.Nested(system_event), description="an array of system events"
            ),
            "meta": fields.Nested(
                get_meta_model(ns), description="information about the returned results"
            ),
        },
    )
