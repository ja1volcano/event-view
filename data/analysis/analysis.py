import json
from typing import Literal
import polars as pl
from functools import partial


def export_results(df: pl.DataFrame, path: str) :
    df.write_json(path)

def findVal(df_warn: str, df_dco_warn: dict) -> str:
    found_key = next((key for key in df_dco_warn if key in df_warn), None)
    if found_key:
        return df_dco_warn[found_key]
    else:
        return ""

def build_event_table_df() -> dict[str, pl.DataFrame]:
    with open('./data/events.json','r') as file:
        raw_data = json.load(file)

    events_raw = pl.DataFrame(raw_data).with_columns(
        pl.col('time_stamp').str.to_datetime().alias('time_stamp')
    )
    with open('./data/event_lut.json','r') as file:
        raw_data = json.load(file)
    df_event_lut = pl.DataFrame(raw_data)

    with open('./data/goes_lut.json','r') as file:
        raw_data = json.load(file)
    df_goes_lut = pl.DataFrame(raw_data).with_columns(
        pl.col('goes_id').str.to_uppercase().alias('goes_id')
    )
    with open('./data/station_lut.json','r') as file:
        raw_data = json.load(file)
    df_station_lut = pl.DataFrame(raw_data)

    with open('./data/analysis/warning_dco.json','r') as file:
        df_dco_warn = json.load(file)    

    _get_warning = partial(findVal, df_dco_warn=df_dco_warn)
    df_goes_lut_filtered = df_goes_lut.filter(~pl.col('is_deleted'))

    event_view_table = (
        events_raw
        .join(
            other=df_event_lut,
            on='sntl_event_key',
            how='left'
        )
        .with_columns(
            pl.col('message').str.split('\'').list.get(1, null_on_oob=True)
                    .str.slice(0,8).alias('goes_id')
        )
        .join(
            other=df_goes_lut_filtered[['goes_id', 'station_id', 'data_to_group_channel']],
            on='goes_id',
            how='left'
        ).with_columns(
            pl.col('station_id').alias('ntwk_sta_id')
        ).join(
            other = df_station_lut[['dco_cd', 'sta_nm', 'ntwk_sta_id']],
            on='ntwk_sta_id',
            how='left'
        ).select(
            pl.col('time_stamp').alias('Date and Time'),
            pl.col('sta_nm').alias('Station Name'),
            pl.col('event_name').alias('Event Name'),
            pl.col('station_id').alias('Station ID'),
            pl.col('dco_cd').alias('Data Collection Office'),
            pl.col('sntl_event_desc').alias('Event Description'),
            pl.col('message').map_elements((lambda x: _get_warning(x))).alias('Error/Warning'),
            pl.col('message').alias('Detailed Message'),
            pl.col('goes_id').alias('GOES ID'),
            pl.col('data_to_group_channel').alias('AWDB Mapping Code'),
        ).with_row_index()
    )
    return {'events_table' :event_view_table}


# def load_data() :
# with open('./data/events.json','r') as file:
#     raw_data = json.load(file)

# df = pl.DataFrame(raw_data).with_columns(
#     pl.col('time_stamp').str.to_datetime().alias('time_stamp')
# )

# dcs_errors = df.filter(pl.col('sntl_event_desc') == 'OPENDCS_ERROR')
# inv_messanges = dcs_errors.filter(
#     pl.col('message').str.contains('Spec says format B but numHours=')
# )


# with open('./data/event_lut.json','r') as file:
#     raw_data = json.load(file)
# df_event_lut = pl.DataFrame(raw_data)

# with open('./data/goes_lut.json','r') as file:
#     raw_data = json.load(file)
# df_goes_lut = pl.DataFrame(raw_data).with_columns(
#     pl.col('goes_id').str.to_uppercase().alias('goes_id')
# )

# with open('./data/station_lut.json','r') as file:
#     raw_data = json.load(file)
# df_station_lut = pl.DataFrame(raw_data)

# with open('./data/analysis/warning_dco.json','r') as file:
#     df_dco_warn = json.load(file)
# # df_dco_warn = pl.DataFrame(raw_data)



# df_results = df.join(
#     other=df_event_lut,
#     on='sntl_event_key',
#     how='left'
# ).with_columns(
#     pl.col('message').str.split('\'').list.get(1, null_on_oob=True)
#                 .str.slice(0,8).alias('goes_id')
# )
# df_goes_lut_filtered = df_goes_lut.filter(~pl.col('is_deleted'))
# final = df_results.join(
#     other=df_goes_lut_filtered[['goes_id', 'station_id', 'data_to_group_channel']],
#     on='goes_id',
#     how='left'
# ).with_columns(
#     pl.col('station_id').alias('ntwk_sta_id')
# ).join(
#     other = df_station_lut[['dco_cd', 'sta_nm', 'ntwk_sta_id']],
#     on='ntwk_sta_id',
#     how='left'
# ).select(
#     pl.col('time_stamp').alias('Date and Time'),
#     pl.col('sta_nm').alias('Station Name'),
#     pl.col('event_name').alias('Event Name'),
#     pl.col('station_id').alias('Station ID'),
#     pl.col('dco_cd').alias('Data Collection Office'),
#     pl.col('sntl_event_desc').alias('Event Description'),
#     pl.col('message').map_elements((lambda x: findVal(x))).alias('Error/Warning'),
#     pl.col('message').alias('Detailed Message'),
#     pl.col('goes_id').alias('GOES ID'),
#     pl.col('data_to_group_channel').alias('AWDB Mapping Code'),
# ).with_row_index()
# export_results(final, './vite-project/data/all_data.json')


# ### agregate by hour
# agg_by_hour_and_dco = final.group_by(
#         pl.col('Date and Time').dt.truncate('1h'),
#         pl.col('Station ID')
#     ).agg(
#         pl.col('Station Name').first(),
#         pl.count().alias('Event Count'),
#         pl.col('Data Collection Office').first(),
#         pl.col('Event Name') , #.first().alias('Event Name'),
#         pl.col('Event Description').alias('Event Description'),
#         pl.col('Error/Warning').alias('Error/Warning'),
#         pl.col('Detailed Message').alias('Detailed Message'),
#         pl.col('GOES ID').first(),
#         pl.col('AWDB Mapping Code').first()
#         # pl.col('Station Name').first().alias('Station Name'),
#         # pl.col('Data Collection Office').first().alias('Data Collection Office'),
#         # pl.col('Event Description').first().alias('Event Description'),
#         # pl.col('Error/Warning').first().alias('Error/Warning'),
#         # pl.col('Detailed Message').first().alias('Detailed Message'),
#         # pl.col('GOES ID').first().alias('GOES ID'),
#         # pl.col('AWDB Mapping Code').first().alias('AWDB Mapping Code')
#     )

def get_station_time_aggregate(df: pl.DataFrame) -> pl.DataFrame:
    return df.group_by(
            pl.col('Date and Time').dt.truncate('1h'),
            pl.col('Station ID')
        ).agg(
            pl.col('Station Name').first(),
            pl.count().alias('Event Count'),
            pl.col('Data Collection Office').first(),
            pl.col('Event Name') , #.first().alias('Event Name'),
            pl.col('Event Description').alias('Event Description'),
            pl.col('Error/Warning').alias('Error/Warning'),
            pl.col('Detailed Message').alias('Detailed Message'),
            pl.col('GOES ID').first(),
            pl.col('AWDB Mapping Code').first(),
            pl.col('index').alias('index')
        )

def group_stations_by_eventhours(df: pl.DataFrame) -> pl.DataFrame:
    return df.group_by(
        pl.col('Station ID')
    ).agg(
        pl.col('Station Name').first(),
        pl.col('Data Collection Office').first(),
        pl.count().alias('Total Hours of Errors over 30 days'),
        pl.col('Event Description').flatten().unique().alias('Unique Event Descriptions'),
        pl.col('index'),
    )



if __name__ == "__main__" or __name__ == "builtins" :
    data_dct = build_event_table_df()
    data_dct['aggregate_by_hour_and_station'] = get_station_time_aggregate(data_dct['events_table'])
    data_dct['station_events_over_30_days'] = group_stations_by_eventhours(data_dct['aggregate_by_hour_and_station'])
    for key, df in data_dct.items():
        export_results(df, f'./vite-project/data/{key}.json')