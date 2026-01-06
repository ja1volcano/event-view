
import { dataStorage } from '../main'
import htmlTemplate from './eventTable.html?raw'
import {TabulatorFull as Tabulator} from 'tabulator-tables'
import './model'
import Plotly from 'plotly.js-dist-min'
import 'tabulator-tables/dist/css/tabulator.min.css'
import 'fsa-style/dist/css/fsa-style.css'
// import eventLut from  "../data/event_lut.json"

export class EventTable extends HTMLElement  {
    static observedAttributes = ["data-ready"]

    constructor() {
        super();
        console.log('this happening?')
    }

    connectedCallback() {
        this.innerHTML = htmlTemplate
    }

    attributeChangedCallback(name, oldValue, newValue) {
        console.log(`Attribute ${name} has changed.`);
        if (name = 'data-ready') {
            this.buildEventtable()
            this.buildStationHourAggTable()
            this.buildStation30DayAggTable()
            this.buildPlotlyChart()
        }
    }

    buildPlotlyChart() {
        const stationIssues = dataStorage['station_events_over_30_days']
        const dcoArray = new Set(stationIssues.map(item => item['Data Collection Office']))
        console.log(dcoArray)
        const stationCount = Array.from(dcoArray).map(dco => {
            return stationIssues.filter(station => station['Data Collection Office'] === dco).length
        })
        const data = [
            {
                // x: dcoArray,
                // y: stationCount,
                // labels: dcoArray,
                x: Array.from(dcoArray),
                y: stationCount,
                type: 'bar',

            }]
        const layout = {
            title: {
                text: 'Number of Stations with Errors Over the Last 30 Days'
            },
            xaxis: {
                title: {
                    text: 'Data Collection Office' 
                },
            },
            yaxis: {
                title: {
                    text: 'Station Count' 
                }
            }
        }
        const config = { responsive: true }
        Plotly.newPlot(this.querySelector('#summary-plot'), data, layout, config)     
    }

    buildEventtable() {
        const arrayOfEvents = dataStorage['event_table']
        var table = new Tabulator(this.querySelector('#event-table'), {
            data:arrayOfEvents, //assign data to table
            layout:"fitColumns",
            pagination:"local",
            paginationSize:25,
            paginationSizeSelector:[25, 50, 75, 100],
            movableColumns:true,
            paginationCounter:"rows",
            
            autoColumns:true, //create columns from data field names
        })
    }

    buildStationHourAggTable() {
        const arrayOfEvents = dataStorage['aggregate_by_hour_and_station']
        var table = new Tabulator(this.querySelector('#station-hour-aggregate-table'), {
            data:arrayOfEvents, //assign data to table
            layout:"fitColumns",
            pagination:"local",
            paginationSize:25,
            paginationSizeSelector:[25, 50, 75, 100],
            movableColumns:true,
            paginationCounter:"rows",
            
            autoColumns:true, //create columns from data field names
        })        
    }

    buildStation30DayAggTable() {
        const button = (cell, formatterParams) =>{ //plain text value
            return "<button class='fsa-btn fsa-btn--secondary'>Show Events</button>"
        }
        const arrayOfEvents = dataStorage['station_events_over_30_days']
        const table = new Tabulator(this.querySelector('#station-30day-aggregate-table'), {
            data:arrayOfEvents, //assign data to table
            layout:"fitColumns",
            pagination:"local",
            paginationSize:25,
            paginationSizeSelector:[25, 50, 75, 100],
            movableColumns:true,
            paginationCounter:"rows",
            // autoColumns:true
            columns:[
                {title:"Station Name", field:"Station Name", formatter:"plaintext"},
                {title:"Station ID", field:"Station ID", formatter:"plaintext"},
           
                {title:"Data Collection Office", field:"Data Collection Office", formatter:"plaintext"},
                {title:"Total Hours of Errors over 30 days", field:"Total Hours of Errors over 30 days", formatter:"plaintext"},
                {title:"Unique Event Descriptions", field:"Unique Event Descriptions", formatter:"array"},
                {title:"Show Events",formatter:button, hozAlign:"center", cellClick:this.showDetailsButton.bind(null, dataStorage['event_table'], arrayOfEvents)}, 
            ]
        })

    }
    showDetailsButton = (eventArray, agg30day, pointerEvent, cell) => {
        console.log('event array:',eventArray)
        console.log('agg array:',agg30day)
        const id = cell.getData()['Station ID']
        console.log('station id:', id)
        const indexLoc = agg30day.filter(row => row['Station ID'] === id)[0].index.flat()
        console.log('index loc:', indexLoc)
        const filteredArray = eventArray.filter(row => indexLoc.includes(row['index']))
        
        console.log(filteredArray)
        const model = this.querySelector('sub-table-dialog-modal')
        model.showModal(cell.getElement(), filteredArray)
    }


  
}