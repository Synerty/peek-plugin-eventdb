import {CommonModule} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {RouterModule, Routes} from "@angular/router";
import {EditSettingComponent} from "./edit-setting-table/edit.component";
// Import our components
import {EventDBComponent} from "./eventdb.component";
import {StatusComponent} from "./status/status.component";
import {
    TupleActionPushNameService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    TupleDataOfflineObserverService
} from "@synerty/vortexjs";

import {
    eventdbActionProcessorName,
    eventdbFilt,
    eventdbObservableName,
    eventdbTupleOfflineServiceName
} from "@peek/peek_plugin_eventdb/_private";

export function tupleActionPushNameServiceFactory() {
    return new TupleActionPushNameService(
        eventdbActionProcessorName, eventdbFilt);
}

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService(
        eventdbObservableName, eventdbFilt);
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService(eventdbTupleOfflineServiceName);
}

// Define the routes for this Angular module
export const pluginRoutes: Routes = [
    {
        path: '',
        component: EventDBComponent
    }

];

// Define the module
@NgModule({
    imports: [
        CommonModule,
        RouterModule.forChild(pluginRoutes),
        FormsModule
    ],
    exports: [],
    providers: [
        TupleActionPushService, {
            provide: TupleActionPushNameService,
            useFactory: tupleActionPushNameServiceFactory
        },
        TupleOfflineStorageService, {
            provide: TupleOfflineStorageNameService,
            useFactory: tupleOfflineStorageNameServiceFactory
        },
        TupleDataObserverService, TupleDataOfflineObserverService, {
            provide: TupleDataObservableNameService,
            useFactory: tupleDataObservableNameServiceFactory
        },
    ],
    declarations: [EventDBComponent, StatusComponent, EditSettingComponent]
})
export class EventDBModule {

}
