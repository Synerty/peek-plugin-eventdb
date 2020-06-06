import {Component, OnInit, Output, EventEmitter} from "@angular/core";
import {EventDBPropertyTuple} from "@peek/peek_plugin_eventdb/tuples";
import {PrivateEventDBService} from "@peek/peek_plugin_eventdb/_private/PrivateEventDBService";
import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";

export interface ColumnI {
    selectedProps: EventDBPropertyTuple[];
}

@Component({
    selector: "plugin-eventdb-event-column",
    templateUrl: "event-column.component.web.html",
    styleUrls: ["../event-common.component.web.scss"],
    moduleId: module.id
})
export class EventDBColumnComponent extends ComponentLifecycleEventEmitter implements OnInit {

    isVisible = false;
    isOkLoading = false;

    props: EventDBPropertyTuple[] = [];
    selectingProps: EventDBPropertyTuple[] = [];

    // TODO: have this coded in a single source with @Input()
    modelSetKey = "pofDiagram";

    @Output("columnChange")
    columnChange = new EventEmitter<ColumnI>();

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private eventService: PrivateEventDBService) {

        super();
    }

    ngOnInit() {
        this.eventService.propertyTuples(this.modelSetKey)
            .takeUntil(this.onDestroyEvent)
            .subscribe((props: EventDBPropertyTuple[]) => {
                this.props = props
                    .sort((a, b) => a.order - b.order);

                this.selectingProps = this.props
                    .filter(prop => prop.displayByDefaultOnDetailView);
            });

    }

    showModal(): void {
        this.isVisible = true;
    }

    onOkClicked(): void {
        this.isOkLoading = true;

        this.columnChange.emit({
            selectedProps: this.selectingProps
        });

        setTimeout(() => {
            this.isVisible = false;
            this.isOkLoading = false;
        }, 500);
    }

    resetDefaults(): void {
        this.isOkLoading = true;

        this.selectingProps = this.props
            .filter(prop => prop.displayByDefaultOnDetailView);
    }

    onCancelClicked(): void {
        this.selectingProps = [];
        this.isVisible = false;
    }
}
