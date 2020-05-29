import {Component, OnInit} from "@angular/core";
import {PrivateEventDBService} from "@peek/peek_plugin_eventdb/_private/PrivateEventDBService";
import {EventDBEventTuple} from "@peek/peek_plugin_eventdb/tuples";
import {DocDbPopupService, DocDbPopupTypeE} from "@peek/peek_plugin_docdb";
import {eventdbPluginName} from "@peek/peek_plugin_eventdb/_private/PluginNames";

import * as moment from "moment";

// import {
//     DocDbPopupActionI,
//     DocDbPopupTypeE
// } from "@peek/peek_plugin_docdb/DocDbPopupService";
// import * as $ from "jquery";
// import {
//     PopupTriggeredParams,
//     PrivateDocDbPopupService
// } from "@peek/peek_plugin_docdb/_private/services/PrivateDocDbPopupService";
// import {NzContextMenuService} from "ng-zorro-antd";
// import {DocDbPopupClosedReasonE, DocDbPopupDetailI} from "@peek/peek_plugin_docdb";


@Component({
    selector: 'plugin-eventdb-event-list',
    templateUrl: 'event-list.component.web.html',
    styleUrls: ['event-list.component.web.scss'],
    moduleId: module.id
})
export class EventDBEventListComponent implements OnInit {

    private lastSubscription = null;
    events = [];
    props = [];

    modelSetKey = 'pofDiagram'

    constructor(private objectPopupService: DocDbPopupService,
                private eventService: PrivateEventDBService) {

    }

    ngOnInit() {
        this.update();
        this.eventService.propertyTuples(this.modelSetKey)
            .subscribe(x => this.props = x);
    }

    private update() {
        if (this.lastSubscription != null)
            this.lastSubscription.unsubscribe();

        const fromDate = moment().subtract(2, 'hours').toDate();

        this.lastSubscription = this.eventService
            .eventTuples(this.modelSetKey,
                {oldestDateTime: fromDate})
            .subscribe((events: EventDBEventTuple[]) => {
                this.events = events;
                for (let event of events) {
                    event.value = JSON.parse(event.value);
                }
            })
    }

    tooltipEnter($event: MouseEvent, result: EventDBEventTuple) {
        if (result.value.component_id == null)
            return;

        const offset = $(".scroll-container").offset();
        this.objectPopupService
            .showPopup(
                DocDbPopupTypeE.tooltipPopup,
                eventdbPluginName,
                {
                    x: $event.x + 50,
                    y: $event.y
                },
                this.modelSetKey,
                result.value.component_id.toLowerCase());

    }

    tooltipExit($event: MouseEvent, result: EventDBEventTuple) {
        this.objectPopupService.hidePopup(DocDbPopupTypeE.tooltipPopup);

    }

    showSummaryPopup($event: MouseEvent, result: EventDBEventTuple) {
        this.objectPopupService.hidePopup(DocDbPopupTypeE.tooltipPopup);
        if (result.value.component_id == null)
            return;

        this.objectPopupService
            .showPopup(
                DocDbPopupTypeE.summaryPopup,
                eventdbPluginName,
                $event,
                this.modelSetKey,
                result.value.component_id.toLowerCase());

    }


}
