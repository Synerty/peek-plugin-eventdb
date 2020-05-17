                                       import {addTupleType, Tuple, TupleActionABC} from "@synerty/vortexjs";
import {eventdbTuplePrefix} from "../PluginNames";

@addTupleType
export class StringCapToggleActionTuple extends TupleActionABC {
    static readonly tupleName = eventdbTuplePrefix + "StringCapToggleActionTuple";

    stringIntId: number;

    constructor() {
        super(StringCapToggleActionTuple.tupleName)
    }
}