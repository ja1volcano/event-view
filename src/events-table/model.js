import {TabulatorFull as Tabulator} from 'tabulator-tables'


export class BaseModal extends HTMLElement {

    constructor(modelClassExtension = 'fsa-modal') {
        super()
        this.innerModelHTML = ''
        this.modelClassExtension = modelClassExtension
        this.trggerElement = undefined
        this.eventListenFunctions = {}
    }

    connectedCallback() {
        this.innerHTML = this.domContainerHtml()
        this.querySelector('.fsa-modal__close').addEventListener('click', this.closeButtonClick)
        this.applyAllEventListeners()
    }

    disconnectedCallback() {
        this.querySelector('.fsa-modal__close').removeEventListener('click', this.closeButtonClick)
        this.removeAllEventListeners()
    }

    closeButtonClick = (event) => {
        if (!this.trggerElement) { 
            console.error('Developer Error: Make sure to pass event trigger element to showModal') }
            const container = event.target.closest('.fsa-modal[role="dialog"]')
            container.ariaHidden = true
            container.ariaExpanded = false
            this.trggerElement.focus()
            this.trggerElement = undefined
        if (document.querySelectorAll('.fsa-modal[role="dialog"][aria-hidden="false"]').length === 0) {
            document.body.classList.remove("fsa-modal-scroll-fix")
        }
    }

    showModal(trggerElement, jsonState) {
        this.trggerElement = trggerElement
        this.jsonStateObject = jsonState
        const container = this.querySelector('.fsa-modal')
        container.ariaHidden = false
        container.ariaExpanded = true
        document.body.classList.add("fsa-modal-scroll-fix")
        this.setFocus(this.querySelector('.fsa-modal__close'))
    }

    async setFocus(element) {
        await new Promise(resolve => setTimeout(resolve, 100))
        element.focus()
    }

    updateJsonStateObject(data = undefined) {
        const event = new CustomEvent('update', {
            detail: data,
            bubbles: true,
            composed: true
        })
        this.dispatchEvent(event)
    }

    domContainerHtml() {
        return /*html*/`
        <div
            tabindex="0"
            class="fsa-modal ${this.modelClassExtension}"
            role="dialog"
            aria-hidden="true"
        >
            <div class="fsa-modal__dialog">
                <div class="fsa-modal__content">
                    <button
                        class="fsa-modal__close"
                        data-behavior="close-modal"
                        title="Close Modal"
                        aria-label="Close Modal"
                        type="button"
                    ></button>
                    <div class="modal-conntent">${this.innerModelHTML}</div>
                </div>
            </div>
        </div>
        `
    }

    // loops through all event listeners and add them to DOM
    applyAllEventListeners() {
        Object.entries(this.eventListenFunctions).forEach(([key, eventArray]) => {
            const elements = this.querySelectorAll(key)
            const captureEvent = eventArray[2] ? eventArray[2] : false
            elements.forEach(element => {
                element.addEventListener(eventArray[0], eventArray[1], captureEvent)
            })
        })
    }

    // remove all event listerns from the DOM
    removeAllEventListeners() {
        Object.entries(this.eventListenFunctions).forEach(([key, eventArray]) => {
            const elements = this.querySelectorAll(key)
            elements.forEach(element => {
                element.removeEventListener(eventArray[0], eventArray[1])
            })
        })
    }
}

export class SubTableDialogeModal extends BaseModal {

    constructor() {
        super('fsa-modal--fullscreen')
    }

    connectedCallback() {
        this.innerModelHTML = this.ModalHtml()
        super.connectedCallback()
    }

    disconnectedCallback() {
        super.disconnectedCallback()
        if (this.table) {
            this.table.destroy()
        }
    }

    showModal(trggerElement, jsonState) {
        super.showModal(trggerElement, jsonState)
        this.buildSubTable(jsonState)
    }


    buildSubTable(data) {
        this.querySelector('h1').innerHTML = data[0]['Station Name']
        var table = new Tabulator(this.querySelector('#sub-table'), {
            data: data, //assign data to table
            height: "80vh",
            layout:"fitColumns",
            pagination:"local",
            paginationSize:25,
            paginationSizeSelector:[25, 50, 75, 100],
            movableColumns:true,
            paginationCounter:"rows",
            autoColumns:true
            // columns:[
            //     {title:"Station Name", field:"Station Name", formatter:"plaintext"},
            //     {title:"Station ID", field:"Station ID", formatter:"plaintext"},
           
            //     {title:"Data Collection Office", field:"Data Collection Office", formatter:"plaintext"},
            //     {title:"Total Hours of Errors over 30 days", field:"Total Hours of Errors over 30 days", formatter:"plaintext"},
            //     {title:"Unique Event Descriptions", field:"Unique Event Descriptions", formatter:"array"},
            //     {title:"Show Events",formatter:button, hozAlign:"center", cellClick:this.showDetailsButton.bind(null, dataStorage['event_table'], arrayOfEvents)}, 
            // ]

        })
        this.table = table
    }


    ModalHtml() {
        return `
        
        <div style="margin: 25px 25px">
            <h1 style="text-align: center;">Events for Station</h1>
            <br>
            <div id="sub-table"></div>
        </div>
        `
    }
}

customElements.define('sub-table-dialog-modal', SubTableDialogeModal)
