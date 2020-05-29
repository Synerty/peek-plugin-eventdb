import {addTupleType, Tuple} from "@synerty/vortexjs";
import {eventdbTuplePrefix} from "../PluginNames";


@addTupleType
export class AdminStatusTuple extends Tuple {
    public static readonly tupleName = eventdbTuplePrefix + "AdminStatusTuple";

    addedEvents: number;
    removedEvents: number;
    lastActivity: Date;

    constructor() {
        super(AdminStatusTuple.tupleName)
    }
}
