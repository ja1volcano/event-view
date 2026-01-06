import eventData from  "../data/events_table.json"
import hourStationAggData from  "../data/aggregate_by_hour_and_station.json"
import station30DayAggData from "../data/station_events_over_30_days.json"
import { EventTable } from "./events-table/eventTable"
import '../node_modules/fsa-style/dist/css/fsa-style.css'

export const dataStorage = {}

customElements.define("event-table", EventTable)

dataStorage['event_table'] = eventData //test2
dataStorage['aggregate_by_hour_and_station'] = hourStationAggData
dataStorage['station_events_over_30_days'] = station30DayAggData

document.querySelector('event-table').toggleAttribute('data-ready')


