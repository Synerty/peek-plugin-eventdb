import {addTupleType, Tuple} from "@synerty/vortexjs";
import {eventdbTuplePrefix} from "@peek/peek_plugin_eventdb/_private/PluginNames";


@addTupleType
export class AdminStatusTuple extends Tuple {
    public static readonly tupleName = eventdbTuplePrefix + "AdminStatusTuple";

    rawValueQueueStatus: boolean;
    rawValueQueueSize: number;
    rawValueProcessedTotal: number;
    rawValueLastError: string;

    constructor() {
        super(AdminStatusTuple.tupleName)
    }
}