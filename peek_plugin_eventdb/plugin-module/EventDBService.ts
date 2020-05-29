import {Observable} from "rxjs";
import {EventDBPropertyCriteriaTuple} from "./tuples/EventDBPropertyCriteriaTuple";
import {EventDBEventTuple} from "./tuples/EventDBEventTuple";
import {EventDateTimeRangeI} from "./_private/PrivateEventDBService";
import {EventDBPropertyTuple} from "./tuples/EventDBPropertyTuple";

/** EventDB Service
 *
 * This class is responsible for providing EventDB information to other plugins
 * and the events list in this plugin.
 *
 */
export abstract class EventDBService {

    /** Property Tuples
     *
     * Return an observable that fires with a list of property tuples.
     *
     * @param modelSetKey: The model to observe the data from.
     */
    abstract propertyTuples(modelSetKey: string): Observable<EventDBPropertyTuple[]> | null;

    /** Event Tuples
     *
     *
     * @param modelSetKey: The key of the model set to load data from.
     * @param dateTimeRange: The dateTime window to load events from.
     * @param criteria: Additional criteria to filter out events.
     */
    abstract eventTuples(
        modelSetKey: string,
        dateTimeRange: EventDateTimeRangeI,
        criteria: EventDBPropertyCriteriaTuple[]): Observable<EventDBEventTuple[]> ;
}



