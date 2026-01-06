# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""

from flask_restx import fields

from core.utils import get_lut
from database import get_connection_ctx

print(
    "-> Querying the database for /lookupTable endpoint data,",
    "any changes to this data will not be reflected until the app is restarted",
)
with get_connection_ctx() as engine:
    master_lut = get_lut(
        table_name="sntl_master_lut",
        key_col="master_id",
        val_cols=("master_nm", "description", "is_active"),
        engine=engine,
    )

    event_lut = get_lut(
        table_name="sntl_event_lut",
        key_col="sntl_event_key",
        val_cols=("event_name", "description_of_event"),
        engine=engine,
    )

    stations_lut = get_lut(
        table_name="awdb_sta_lut",
        key_col="ntwk_sta_id",
        val_cols=(
            "awdb_sta_key",
            "sta_nm",
            "st_key",
            "ntwk_key",
            "dco_cd",
            "tm_zone",
            "lat",
            "lon",
            "elev",
            "in_srvc_dt",
            "out_srvc_dt",
            "rmk",
            "huc",
        ),
        engine=engine,
    )

    goes_lut = get_lut(
        table_name="sntl_lrgs_station_configuration",
        key_col="station_id",
        val_cols=(
            "goes_id",
            "is_goes_enabled",
            "data_to_group_channel",
            "midnight_group",
            "lrgs_message_format_cd",
            "is_deleted",
            "last_updated",
            "updated_by",
        ),
        engine=engine,
    )

    iridium_lut = get_lut(
        table_name="sntl_lrgs_station_configuration",
        key_col="station_id",
        val_cols=(
            "iridium_imei",
            "is_iridium_enabled",
            "data_to_group_channel",
            "midnight_group",
            "lrgs_message_format_cd",
            "is_deleted",
            "last_updated",
            "updated_by",
        ),
        engine=engine,
    )


class LookupField(fields.Raw):
    def __init__(self, key, lut, attr_key=None, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.lut = lut
        self.attr_key = attr_key

    def output(self, key, obj, *args, **kwargs):
        key_value = getattr(obj, self.key, None)
        if key_value in self.lut:
            lookup_val = self.lut[key_value]
            if self.attr_key and isinstance(lookup_val, dict):
                return lookup_val[self.attr_key]
            return lookup_val
        return None
