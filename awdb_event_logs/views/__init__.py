# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:09:07 2021

@author: Beau.Uriona
"""
from flask_restx import Api


def create_api():
    api = Api(
        version="1.0",
        title="SNOTEL Event Logs API",
        description="A basic API for retrieving SNOTEL event log items from AWDB",
    )
    from . import logs, luts

    api.add_namespace(logs.ns)
    api.add_namespace(luts.ns)

    return api
