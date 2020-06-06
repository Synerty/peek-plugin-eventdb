import {Component, EventEmitter, OnInit, Output} from "@angular/core";
import {PrivateEventDBService} from "@peek/peek_plugin_eventdb/_private/PrivateEventDBService";
import {
    EventDBPropertyCriteriaTuple,
    EventDBPropertyShowFilterAsEnum,
    EventDBPropertyTuple
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
    styleUrls: ["event-filter.component.web.scss",
        "../event-common.component.web.scss"],
    moduleId: module.id
})
export class EventDBFilterComponent extends ComponentLifecycleEventEmitter implements OnInit {

    isVisible = false;
    isOkLoading = false;

    props: EventDBPropertyTuple[] = [];
    filterProps: EventDBPropertyTuple[] = [];

    private propCriteria: { [key: string]: EventDBPropertyCriteriaTuple } = {};

    dateTimeRange: EventDateTimeRangeI;

    private criterias: EventDBPropertyCriteriaTuple[] = [];

    // TODO: have this coded in a single source with @Input()
    modelSetKey = "pofDiagram";

    private liveUpdateTimer: any;
    private liveEnabled: boolean = true;

    @Output("filterChange")
    filterChange = new EventEmitter<FilterI>();

    FilterAsEnum = EventDBPropertyShowFilterAsEnum;

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private eventService: PrivateEventDBService) {

        super();

    }

    ngOnInit() {
        this.dateTimeRange = {
            oldestDateTime: moment().subtract(2, "hours").toDate(),
            newestDateTime: null,
        };

        this.eventService.propertyTuples(this.modelSetKey)
            .takeUntil(this.onDestroyEvent)
            .subscribe((props: EventDBPropertyTuple[]) => {
                this.props = props;

                // filter for default filter properties.
                this.filterProps = props
                    .filter(prop => prop.useForFilter)
                    .sort((a, b) => a.order - b.order);
            });


        // Setup a timer to update the last hour of data.
        // If someone leaves the alarm list over night, the earliest date won't update.
        this.liveUpdateTimer = setInterval(() => this.liveEnabledUpdateTimerCall(),
            10 * 60 * 1000);

        this.onDestroyEvent
            .first()
            .subscribe(() => clearInterval(this.liveUpdateTimer));

    }

    private defaultOldestDateTime(): Date {
        // Round the datetime to the nearest 5 minutes.
        // This will help to reduce the calls for people just watching the events.
        let newDate = moment().subtract(2, "hours").seconds(0);
        let minute = newDate.minute();
        newDate.minute(minute - minute % 5);
        return newDate.toDate();
    }

    private liveEnabledUpdateTimerCall(): void {
        if (!this.liveEnabled)
            return;

        this.dateTimeRange = {
            oldestDateTime: this.defaultOldestDateTime(),
            newestDateTime: null
        };

        this.updateFilter();
    }

    updateLive(liveEnabled: boolean): void {
        this.liveEnabled = liveEnabled;

        if (this.liveEnabled)
            this.liveEnabledUpdateTimerCall()

        else if (this.dateTimeRange.newestDateTime == null)
            this.dateTimeRange.newestDateTime = moment().toDate();

        this.updateFilter();
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

    onOkClicked(): void {
        this.isOkLoading = true;

        if (!this.liveEnabled) {
            if (this.dateTimeRange.oldestDateTime == null)
                this.dateTimeRange.oldestDateTime = this.defaultOldestDateTime();

            if (this.dateTimeRange.newestDateTime == null)
                this.dateTimeRange.newestDateTime = moment().toDate();
        }

        this.criterias = [];
        for (let key of Object.keys(this.propCriteria)) {
            const criteria = this.propCriteria[key];
            // TODO: don't add if value is blank.
            if (criteria.value != null && criteria.value.length != 0)
                this.criterias.push(criteria);
        }

        this.updateFilter();

        setTimeout(() => {
            this.isVisible = false;
            this.isOkLoading = false;
        }, 500);
    }

    private updateFilter() {
        this.filterChange.emit({
            modelSetKey: this.modelSetKey,
            dateTimeRange: this.dateTimeRange,
            criteria: this.criterias,
        });
    }

    resetDefaults(): void {
        this.propCriteria = {};
    }

    onCancelClicked(): void {
        this.isVisible = false;
    }
}
