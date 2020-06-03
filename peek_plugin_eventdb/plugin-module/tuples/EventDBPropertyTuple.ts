import {addTupleType, Tuple} from "@synerty/vortexjs";
import {eventdbTuplePrefix} from "../_private/PluginNames";
import {EventDBPropertyValueTuple} from "./EventDBPropertyValueTuple";

export enum EventDBPropertyShowFilterAsEnum {
    SHOW_FILTER_AS_FREE_TEXT = 1,
    SHOW_FILTER_AS_CHECK_BOXES = 2,
    SHOW_FILTER_AS_DROP_DOWN = 3,
}

/** Event DB Property Tuple

 This tuple stores the name of a property in the alarm / event that the user
 can filter on.

 */
@addTupleType
export class EventDBPropertyTuple extends Tuple {
    public static readonly tupleName = eventdbTuplePrefix + "EventDBPropertyTuple";

    // modelSetKey: The model that this property applies to.
    modelSetKey: string;

    // key: The unique id of this property within this model set, it must match
    //         the value of a key in the EventDBEventTuple.value json object.
    key: string;

    // name: The name to display to the user in a UI.
    name: string;

    // order: The order of this field
    order: number;

    // comment: The tooltip to display to the user in a UI.
    comment: string | null;

    // useForFilter: Can the user type free text in this field ?
    useForFilter: boolean | null;

    // useForDisplay: Can the user choose to see this
    useForDisplay: boolean | null;

    // FOR DISPLAY
    // displayByDefaultOnSummaryView: Is this field visible by default when showing a
    //      summary alarm / event list.
    displayByDefaultOnSummaryView: boolean | null;

    // FOR DISPLAY
    // displayByDefaultOnDetailView: Is this field visible by default when showing a
    //      details/full alarm / event list.
    displayByDefaultOnDetailView: boolean | null;

    // FOR FILTER
    // showFilterAs: How should the filter be displayed to the user.
    showFilterAs: EventDBPropertyShowFilterAsEnum | null;

    // FOR FILTER and FOR DISPLAY
    // values: the list of values for
    values: EventDBPropertyValueTuple[] | null;
    // Create a map of the values to speed up conversion for the UI.
    private nameByValue: { [value: string]: string };
​

    constructor() {
        super(EventDBPropertyTuple.tupleName);
    }

​

    /** Raw Value To User Value
     *
     * @param value: The raw value in the data
     * @return: The user friendly value
     */
    rawValToUserVal(value: string): string {
        // Lazy create the map
        if (this.nameByValue == null) {
            this.nameByValue = {};
            for (let valueTuple of this.values) {
                this.nameByValue[valueTuple.value] = valueTuple.name;
            }
        }
​
        // Return the name for the value
        return this.nameByValue[value];
    }
}
