import {TabulatorFull as Tabulator} from 'tabulator-tables'


class tableElement extends HTMLElement {

    constructor() {
        super()
        this.columnsToFilter = ['index']
        // this.style.marginBottom = '500px'
    }
    connectedCallback() {
        this.tableId = crypto.randomUUID()
        this.innerHTML = this.domContainerHtml(this.tableId)
        Array.from(this.querySelectorAll('.download-table')).forEach(button => {
            button.addEventListener('click', this.downloadButtonEvent)
        })
        this.querySelector('.reset-table').addEventListener('click', this.resetFilters)
    }

    disconnectedCallback() {
        this.tableId = undefined
        if (this.table) { this.table.destroy()}
        Array.from(this.querySelectorAll('.download-table')).forEach(button => {
            button.removeEventListener('click', this.downloadButtonEvent)
        })
        this.querySelector('.reset-table').removeEventListener('click', this.resetFilters)
    }

    domContainerHtml() {
        this.tableId = 'internal-table'
        return `
            <style>
                #${this.tableId} {
                    height: 80vh;
                    width: 100%;
                    margin: 10px 0px 10px 0px;
                }
                #table-container {
                    margin: 50px 0px 50px 0px;
                }
            </style>
            <div id="table-container">
                <h2></h2>
                <div>
                    <button class="download-table fsa-btn">Download CSV</button>
                    <button class="download-table fsa-btn">Download JSON</button>
                    <button class="download-table fsa-btn">Download HTML</button>
                    <button class="reset-table fsa-btn fsa-btn--secondary">Reset Filters</button>
                </div>
                <p>To reset the column filters, click the column header and then press the escape key.</p>
                <div id=${this.tableId}>
            </div>
        `
    }

    resetFilters = () => {
        this.table.clearHeaderFilter()
    }

    downloadButtonEvent = (event) => {
        const format = event.target.id.split('-')[1].toLowerCase()
        this.table.download(format, `events_table.${format.toLowerCase()}`)
    }

    buildTable(name, jsonData, customColumns = undefined) {
        this.querySelector('h2').innerHTML = name
        customColumns = this.columnSettup(customColumns, jsonData)
        const rowFormatorFunc = this.rowFormatorFunctionGenerator(customColumns)
        const tableDiv = this.querySelector(`#${this.tableId}`)
        this.table = new Tabulator(tableDiv, {
            data: jsonData, 
            rowFormatter: rowFormatorFunc,
            layout:"fitData",
            pagination:"local",
            paginationSize:25,
            paginationSizeSelector:[25, 50, 75, 100],
            movableColumns:true,
            paginationCounter:"rows",
            columns: customColumns
        })        
    }

    rowFormatorFunctionGenerator(customColumns) {
        const titlesForCol = customColumns.map(col => col.title)
        if (titlesForCol.includes('Event Description') || titlesForCol.includes('Unique Event Descriptions')) { 
            
            return (row) => {
                const rowData = row.getData()
                const eventType = rowData['Event Description'] ? rowData['Event Description'] : rowData['Unique Event Descriptions']
                let stringFromEventDescription
                if ('object' === typeof eventType) {
                    stringFromEventDescription = eventType.join()
                } else {
                    stringFromEventDescription = eventType
                }
                if (stringFromEventDescription && stringFromEventDescription.toLowerCase().includes('error')) {
                    row.getElement().style.backgroundColor = "#ffcccc"; // Light red background
                    row.getElement().style.color = "#a00000" 
                } else if (stringFromEventDescription && stringFromEventDescription.toLowerCase().includes('warning')) {
                    row.getElement().style.backgroundColor = "#fff0b3"; // Light yellow background
                    row.getElement().style.color = "#a67c00" 
                }
            }
        }
    }

    columnSettup(customColumnsObj, data) {
        const keys = Object.keys(data[0])
        if (!customColumnsObj) { customColumnsObj = [] }
        const customKeys = customColumnsObj.map(col => col.title)   
        const allColumns = new Set(customKeys.concat(keys))
        const columnObj = []
        allColumns.forEach(key => {
            if(customKeys.includes(key)) {
                columnObj.push(customColumnsObj.find(col => col.title === key))
            } else if ( ['Event Description', 
                'Data Collection Office', 
                'Station Network', 
                'Unique Event Descriptions', 
                "Error/Warning", 
                'Event Associated Telemetry', 
                'Event Name'
            ].includes(key)) {
                columnObj.push({title:key, field:key, formatter:"plaintext",  editor:"input", headerFilterPlaceholder:"click for dropdown...", headerFilter:"list", headerFilterParams:{valuesLookup:true, clearable:true}})
            } else if ( ['Date and Time'].includes(key)) {
                columnObj.push({title:key, field:key, formatter:"plaintext"})
            } else {
                if (!this.columnsToFilter.includes(key)) {
                    columnObj.push({title:key, field:key, formatter:"plaintext", headerFilter:"input"})
                }
            }
        })
        return columnObj
    }
    

}

customElements.define('table-element', tableElement)