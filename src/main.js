// import eventData from  "../public/events_table.json"
// import hourStationAggData from  "../public/aggregate_by_hour_and_station.json"
// import station30DayAggData from "../public/station_events_over_30_days.json"
import { EventTable } from "./events-table/eventTable"
import '../node_modules/fsa-style/dist/css/fsa-style.css'

export const dataStorage = {}

customElements.define("event-table", EventTable)

async function loadData() {
    const promises = [
        fetch('events_table.json').then(i =>i.json()).catch(e => console.error(e)),
        fetch('aggregate_by_hour_and_station.json').then(i =>i.json()).catch(e => console.error(e)),
        fetch('station_events_over_30_days.json').then(i =>i.json()).catch(e => console.error(e))
    ]

    const results = await Promise.all(promises)
    console.log(results)
    dataStorage['event_table'] = results[0]
    dataStorage['aggregate_by_hour_and_station']  = results[1]
    dataStorage['station_events_over_30_days']= results[2]

    document.querySelector('event-table').toggleAttribute('data-ready')
}


loadData()

// dataStorage['event_table'] = eventData //test2
// dataStorage['aggregate_by_hour_and_station'] = hourStationAggData
// dataStorage['station_events_over_30_days'] = station30DayAggData

// document.querySelector('event-table').toggleAttribute('data-ready')


