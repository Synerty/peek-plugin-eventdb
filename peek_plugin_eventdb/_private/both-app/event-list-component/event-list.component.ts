import {Component, OnInit} from "@angular/core";
import {PrivateEventDBService} from "@peek/peek_plugin_eventdb/_private/PrivateEventDBService";
import {EventDBEventTuple, EventDBPropertyTuple} from "@peek/peek_plugin_eventdb/tuples";
import {DocDbPopupService, DocDbPopupTypeE} from "@peek/peek_plugin_docdb";
import {eventdbPluginName} from "@peek/peek_plugin_eventdb/_private/PluginNames";
import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";

import * as moment from "moment";
import {FilterI} from "../event-filter-component/event-filter.component";
import {ColumnI} from "../event-column-component/event-column.component";

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
    selector: "plugin-eventdb-event-list",
    templateUrl: "event-list.component.web.html",
    moduleId: module.id
})
export class EventDBEventListComponent extends ComponentLifecycleEventEmitter implements OnInit {

    private lastSubscription = null;
    events: EventDBEventTuple[] = [];
    props: EventDBPropertyTuple[] = [];
    displayProps: EventDBPropertyTuple[] = [];

    modelSetKey = "pofDiagram";

    constructor(private objectPopupService: DocDbPopupService,
                private eventService: PrivateEventDBService) {
        super();
    }

    ngOnInit() {
        this.updateFilter({
            modelSetKey: this.modelSetKey,
            dateTimeRange: {
                oldestDateTime: moment().subtract(2, "hours").toDate(),
                newestDateTime: null,
            },
            criteria: [],
        });

        this.eventService.propertyTuples(this.modelSetKey)
            .takeUntil(this.onDestroyEvent)
            .subscribe((props: EventDBPropertyTuple[]) => {

                // sort properties by order.
                this.props = props.sort((a, b) => a.order - b.order);

                // filter for default display properties.
                this.updateColumn({
                    selectedProps: props
                        .filter(prop => prop.displayByDefaultOnDetailView)
                        .sort((a, b) => a.order - b.order)
                });
            });
    }

    updateColumn(props: ColumnI) {
        this.displayProps = props.selectedProps;
    }

    updateFilter(filter: FilterI) {
        if (this.lastSubscription != null)
            this.lastSubscription.unsubscribe();

        this.lastSubscription = this.eventService
            .eventTuples(filter.modelSetKey, filter.dateTimeRange, filter.criteria)
            .subscribe((events: EventDBEventTuple[]) => {
                this.events = events;
                for (let event of events) {
                    event.value = JSON.parse(event.value);
                }
            });
    }

    displayValue(event: EventDBEventTuple, prop: EventDBPropertyTuple): string {
        const eventVal = event.value[prop.key];
        if (prop.values != null)
            return eventVal;
​
        return prop.values != null ? eventVal : prop.rawValToUserVal(eventVal);
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
