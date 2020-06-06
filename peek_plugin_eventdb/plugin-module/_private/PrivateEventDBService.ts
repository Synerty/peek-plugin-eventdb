import {Injectable} from "@angular/core";
import {ComponentLifecycleEventEmitter, TupleSelector} from "@synerty/vortexjs";
import {BehaviorSubject, Observable} from "rxjs";
import {EventDBPropertyTuple} from "../tuples/EventDBPropertyTuple";
import {EventDBPropertyCriteriaTuple} from "../tuples/EventDBPropertyCriteriaTuple";
import {EventDBEventTuple} from "../tuples/EventDBEventTuple";
import {EventDateTimeRangeI, EventDBService} from "../EventDBService";
import {EventDBTupleService} from "./EventDBTupleService";
import {map} from "rxjs/operators";


@Injectable()
export class PrivateEventDBService extends ComponentLifecycleEventEmitter
    implements EventDBService {

    private _propertiesByModelSetKey: { [modelSetKey: string]: EventDBPropertyTuple[] } = {};
    private _subjectByModelSetKey: { [modelSetKey: string]: BehaviorSubject<EventDBPropertyTuple[]> } = {};

    private _isReady: boolean = false;


    constructor(private tupleService: EventDBTupleService) {
        super();
        this.initialLoad();
    }

    shutdown(): void {
    }

    isReady(): boolean {
        return this._isReady;
    }

    private initialLoad(): void {

        const ts = new TupleSelector(EventDBPropertyTuple.tupleName, {});

        this.tupleService.offlineObserver
            .subscribeToTupleSelector(ts)
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: EventDBPropertyTuple[]) => {
                this._propertiesByModelSetKey = {};
                const dict = this._propertiesByModelSetKey;

                for (let item of tuples) {
                    // Coord Set by Coord Set Key, by Model Set Key
                    const data = dict[item.modelSetKey] == null
                        ? dict[item.modelSetKey] = []
                        : dict[item.modelSetKey];

                    data.push(item);
                }

                this._isReady = tuples.length != 0;
                for (let key of Object.keys(dict)) {
                    const subject = this._subjectByModelSetKey[key];
                    if (subject != null)
                        subject.next(dict[key]);
                }
            });
    }

    propertyTuples(modelSetKey: string): Observable<EventDBPropertyTuple[]> | null {
        if (this._subjectByModelSetKey[modelSetKey] == null) {
            const props = this._propertiesByModelSetKey[modelSetKey];
            this._subjectByModelSetKey[modelSetKey]
                = new BehaviorSubject<EventDBPropertyTuple[]>(props || []);
        }

        const subject = this._subjectByModelSetKey[modelSetKey];
        return subject ? subject : null;
    }

    eventTuples(modelSetKey: string,
                dateTimeRange: EventDateTimeRangeI | null = null,
                criteria: EventDBPropertyCriteriaTuple[] = []): Observable<EventDBEventTuple[]> {
        if (modelSetKey == null || modelSetKey.length === 0) {
            throw new Error("eventTuples: modelSetKey argument is null" +
                " or an empty string");
        }

        const ts = new TupleSelector(EventDBEventTuple.tupleName, {
            modelSetKey: modelSetKey,
            newestDateTime: dateTimeRange != null ? dateTimeRange.newestDateTime : null,
            oldestDateTime: dateTimeRange != null ? dateTimeRange.oldestDateTime : null,
            criteria: criteria
        });

        const observable: Observable<EventDBEventTuple[]> =
            <Observable<EventDBEventTuple[]>>this.tupleService
                .offlineObserver
                .subscribeToTupleSelector(ts)
                .takeUntil(this.onDestroyEvent);

        return observable
            .pipe(map((events: EventDBEventTuple[]) => {
                // Convert the json string to actual json objects
                // Don't do it if it's already done as
                // VortexJS caches the data in memory for a short period.
                if (events != null && events.length != 0) {
                    if (typeof events[0].value === "string") {
                        for (let event of events) {
                            event.value = JSON.parse(event.value);
                        }
                    }
                }
                return events;
            }));

    }
}
