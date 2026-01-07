import {TabulatorFull as Tabulator} from 'tabulator-tables'


class baseTable extends HTMLElement {

    constructor() {
        super()
        this.columnsToFilter = ['index']
    }
    connectedCallback() {
        this.tableId = crypto.randomUUID()
        this.innerHTML = this.domContainerHtml(this.tableId)
    }

    disconnectedCallback() {
        this.tableId = undefined
        if (this.table) { this.table.destroy()}
    }

    domContainerHtml() {
        this.tableId = 'internal-table'
        return `
            <style>
                #${this.tableId} {
                    height: 80vh;
                    width: 100%;
                    margin: 10px;
                }
            </style>
            <h1><h1>
            <div id=${this.tableId}><div>
        `
    }

    buildTable(name, data, customColumns = undefined) {
        this.querySelector('h1').innerHTML = name
        const keys = Object.keys(data[0])
        const keySetPairs = keys.map(key => {
            return [key, new Set(data.map(obj => {
                return obj[key]
            }))]
        })
        const options = new Map(keySetPairs)
        console.log(options)
        if (!customColumns) {
            const item = data[0]
            customColumns = []
            Object.entries(item).forEach(([key, value]) => {
                if (!this.columnsToFilter.includes(key)) {
                    customColumns.push(
                        {title:key, field:key, formatter:"plaintext", headerFilter:"input" }//headerFilterParams:{valuesLookup:true, clearable:true}}
                    )
                }
            })
        }
        console.log('custom columns', customColumns)
        this.table = new Tabulator(this.querySelector(`#${this.tableId}`), {
            data: data, //assign data to table
            // colMinWidth: 200,
            layout:"fitData",
            pagination:"local",
            paginationSize:25,
            paginationSizeSelector:[25, 50, 75, 100],
            movableColumns:true,
            paginationCounter:"rows",
            // autoColumns:true
            columns: customColumns
        })        
    }


}

customElements.define('table-element', baseTable)