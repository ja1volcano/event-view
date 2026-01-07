
import { dataStorage } from '../main'
import htmlTemplate from './eventTable.html?raw'
import {TabulatorFull as Tabulator} from 'tabulator-tables'
import './model'
import './table'
import Plotly from 'plotly.js-dist-min'
import 'tabulator-tables/dist/css/tabulator.min.css'
import 'fsa-style/dist/css/fsa-style.css'
// import eventLut from  "../data/event_lut.json"

export class EventTable extends HTMLElement  {
    static observedAttributes = ["data-ready"]

    constructor() {
        super()
        // console.log('this happening?')
    }

    connectedCallback() {
        this.innerHTML = htmlTemplate
    }

    attributeChangedCallback(name, oldValue, newValue) {
        // console.log(`Attribute ${name} has changed.`);
        if (name = 'data-ready') {
            this.buildEventtable()
            this.buildStationHourAggTable()
            this.buildStation30DayAggTable()
            this.buildPlotlyChart()
        }
        // const customElementTable = this.querySelector('#testTable')
        // customElementTable.buildTable('test',dataStorage['event_table'])
    }

    buildPlotlyChart() {
        const stationIssues = dataStorage['station_events_over_30_days']
        const dcoArray = new Set(stationIssues.map(item => item['Data Collection Office']))
        // console.log(dcoArray)
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
        const customElement = this.querySelector('#event-table')
        const arrayOfEvents = dataStorage['event_table']
        customElement.buildTable('All Event Table', arrayOfEvents)
        // var table = new Tabulator(this.querySelector('#event-table'), {
        //     data:arrayOfEvents, //assign data to table
        //     layout:"fitColumns",
        //     pagination:"local",
        //     paginationSize:25,
        //     paginationSizeSelector:[25, 50, 75, 100],
        //     movableColumns:true,
        //     paginationCounter:"rows",
            
        //     autoColumns:true, //create columns from data field names
        // })
    }

    buildStationHourAggTable() {
        const customElement = this.querySelector('#station-hour-aggregate-table')
        const arrayOfEvents = dataStorage['aggregate_by_hour_and_station']
        customElement.buildTable('Events Aggrigated by Station per Hour', arrayOfEvents)
        // const keySetPairs = Object.keys(arrayOfEvents[0]).map(key => {')
        // var table = new Tabulator(this.querySelector('#station-hour-aggregate-table'), {
        //     data:arrayOfEvents, //assign data to table
        //     layout:"fitColumns",
        //     pagination:"local",
        //     paginationSize:25,
        //     paginationSizeSelector:[25, 50, 75, 100],
        //     movableColumns:true,
        //     paginationCounter:"rows",
            
        //     autoColumns:true, //create columns from data field names
        // })        
    }

    buildStation30DayAggTable() {
        const customElement = this.querySelector('#station-30day-aggregate-table')
        const arrayOfEvents = dataStorage['station_events_over_30_days']
        const button = (cell, formatterParams) => { //plain text value
            return "<button class='fsa-btn fsa-btn--secondary'>Show Events</button>"
        }
        const columns =[
            {title:"Show Events",formatter:button, hozAlign:"center", cellClick:this.showDetailsButton.bind(null, dataStorage['event_table'], arrayOfEvents)},             
        ]

        // console.log('custom columns', columns)
        customElement.buildTable('Events Aggrigate By Station Over 30 days', arrayOfEvents, columns)
        // const table = new Tabulator(this.querySelector('#station-30day-aggregate-table'), {
        //     data:arrayOfEvents, //assign data to table
        //     layout:"fitColumns",
        //     pagination:"local",
        //     paginationSize:25,
        //     paginationSizeSelector:[25, 50, 75, 100],
        //     movableColumns:true,
        //     paginationCounter:"rows",
        //     // autoColumns:true
        //     columns:[
        //         {title:"Station Name", field:"Station Name", formatter:"plaintext", headerFilter:"input"},
        //         {title:"Show Events",formatter:button, hozAlign:"center", cellClick:this.showDetailsButton.bind(null, dataStorage['event_table'], arrayOfEvents)}, 
        //         // {title:"Station ID", field:"Station ID", formatter:"plaintext"},
        //         // {title:"Station Network", field:"Station Network", formatter:"plaintext"},
        //         // {title:"Data Collection Office", field:"Data Collection Office", formatter:"plaintext"},
        //         // {title:"Total Hours of Errors over 30 days", field:"Total Hours of Errors over 30 days", formatter:"plaintext"},
        //         // {title:"Unique Event Descriptions", field:"Unique Event Descriptions", formatter:"array"},
                
        //     ]
        // })

    }
    showDetailsButton = (eventArray, agg30day, _, cell) => {
        const id = cell.getData()['Station ID']
        const indexLoc = agg30day.filter(row => row['Station ID'] === id)[0].index.flat()
        const filteredArray = eventArray.filter(row => indexLoc.includes(row['index']))
        const model = this.querySelector('sub-table-dialog-modal')
        model.showModal(cell.getElement(), filteredArray)
    }


  
}