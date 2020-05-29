import {addTupleType, Tuple} from "@synerty/vortexjs";
import {eventdbTuplePrefix} from "../_private/PluginNames";
import {EventDBPropertyTuple} from "./EventDBPropertyTuple";
import {EventDBPropertyValueTuple} from "./EventDBPropertyValueTuple";


/** Event DB Property Criteria Tuple

 This tuple stores the criteria of alarms and events to retrieve.

 */
@addTupleType
export class EventDBPropertyCriteriaTuple extends Tuple {
    public static readonly tupleName = eventdbTuplePrefix + "EventDBPropertyCriteriaTuple";


    property: EventDBPropertyTuple;
    value: EventDBPropertyValueTuple | string;

    constructor() {
        super(EventDBPropertyCriteriaTuple.tupleName)
    }
}
