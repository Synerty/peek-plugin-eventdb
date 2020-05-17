 import {addTupleType, Tuple, TupleActionABC} from "@synerty/vortexjs";
import {eventdbTuplePrefix} from "../PluginNames";

@addTupleType
export class AddIntValueActionTuple extends TupleActionABC {
    static readonly tupleName = eventdbTuplePrefix + "AddIntValueActionTuple";

    stringIntId: number;
    offset: number;

    constructor() {
        super(AddIntValueActionTuple.tupleName)
    }
}