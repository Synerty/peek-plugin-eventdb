import {Component, OnInit, EventEmitter, Output} from "@angular/core";
import {PrivateEventDBService} from "@peek/peek_plugin_eventdb/_private/PrivateEventDBService";
import {
    EventDBPropertyTuple,
    EventDBPropertyCriteriaTuple,
    EventDBPropertyShowFilterAsEnum
} from "@peek/peek_plugin_eventdb/tuples";
import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {EventDateTimeRangeI} from "@peek/peek_plugin_eventdb";

import * as moment from "moment";

export interface FilterI {
    modelSetKey: string;
    dateTimeRange: EventDateTimeRangeI;
    criteria: EventDBPropertyCriteriaTuple[];
}

@Component({
    selector: "plugin-eventdb-event-filter",
    templateUrl: "event-filter.component.web.html",
    styleUrls: ["../event-common.component.web.scss"],
    moduleId: module.id
})
export class EventDBFilterComponent extends ComponentLifecycleEventEmitter implements OnInit {

    isVisible = false;
    isOkLoading = false;

    props: EventDBPropertyTuple[] = [];
    filterProps: EventDBPropertyTuple[] = [];

    private propCriteria: { [key: string]: EventDBPropertyCriteriaTuple } = {};

    // TODO: have this coded in a single source with @Input()
    modelSetKey = "pofDiagram";

    @Output("filterChange")
    filterChange = new EventEmitter<FilterI>();

    FilterAsEnum = EventDBPropertyShowFilterAsEnum;

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private eventService: PrivateEventDBService) {

        super();
    }

    ngOnInit() {
        this.eventService.propertyTuples(this.modelSetKey)
            .takeUntil(this.onDestroyEvent)
            .subscribe((props: EventDBPropertyTuple[]) => {
                this.props = props;

                // filter for default filter properties.
                this.filterProps = props
                    .filter(prop => prop.useForFilter)
                    .sort((a, b) => a.order - b.order);
            });

    }

    clearFilter() {
        this.propCriteria = {};
    }

    criteria(prop: EventDBPropertyTuple): EventDBPropertyCriteriaTuple {
        if (this.propCriteria[prop.key] == null) {
            this.propCriteria[prop.key] = new EventDBPropertyCriteriaTuple();
            this.propCriteria[prop.key].property = prop;
        }
        return this.propCriteria[prop.key];
    }

    showModal(): void {
        this.isVisible = true;
    }

    handleOk(): void {
        this.isOkLoading = true;

        const criterias: EventDBPropertyCriteriaTuple[] = [];
        for (let key of Object.keys(this.propCriteria)) {
            const criteria = this.propCriteria[key];
            // TODO: don't add if value is blank.
            if (criteria.value != null && criteria.value.length != 0)
                criterias.push(criteria);
        }

        this.filterChange.emit({
            modelSetKey: this.modelSetKey,
            dateTimeRange: {
                oldestDateTime: moment().subtract(2, "hours").toDate(),
                newestDateTime: null,
            },
            criteria: criterias,
        });

        setTimeout(() => {
            this.isVisible = false;
            this.isOkLoading = false;
        }, 500);
    }

    handleCancel(): void {
        this.isVisible = false;
    }
}
