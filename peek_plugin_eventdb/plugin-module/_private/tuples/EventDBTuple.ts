import {addTupleType, Tuple} from "@synerty/vortexjs";
import {eventdbTuplePrefix} from "../PluginNames";


@addTupleType
export class EventDBTuple extends Tuple {
    public static readonly tupleName = eventdbTuplePrefix + "EventDBTuple";

    //  Description of date1
    dict1 : {};

    //  Description of array1
    array1 : any[];

    //  Description of date1
    date1 : Date;

    constructor() {
        super(EventDBTuple.tupleName)
    }
}