import {Component, OnInit} from "@angular/core";
import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";
// import {ActivatedRoute, Params} from "@angular/router";
import {TitleService} from "@synerty/peek-util";


@Component({
    selector: "plugin-eventdb-event-page",
    templateUrl: "event-page.component.web.html",
    styleUrls: ["../event-common.component.web.scss"],

    moduleId: module.id
})
export class EventDBPageComponent extends ComponentLifecycleEventEmitter implements OnInit {

    constructor(private titleService: TitleService) {
        super();

        titleService.setTitle("Alarm and Events");

    }

    ngOnInit() {

        //     this.route.params
        //         .takeUntil(this.onDestroyEvent)
        //         .subscribe((params: Params) => {
        //             let vars = {};
        //
        //             if (typeof window !== 'undefined') {
        //                 window.location.href.replace(
        //                     /[?&]+([^=&]+)=([^&]*)/gi,
        //                     (m, key, value) => vars[key] = value
        //                 );
        //             }
        //
        //             let key = params['key'] || vars['key'];
        //             let modelSetKey = params['modelSetKey'] || vars['modelSetKey'];
        //
        //             this.docDbService.getObjects(modelSetKey, [key])
        //                 .then((docs: DocumentResultI) => this.loadDoc(docs[key], key));
        //
        //         });

    }



}
