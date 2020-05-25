import {CommonModule} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {RouterModule, Routes} from "@angular/router";

import {NzTabsModule} from 'ng-zorro-antd/tabs';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzIconModule} from 'ng-zorro-antd/icon';
import {NzSwitchModule} from 'ng-zorro-antd/switch';
import {NzSelectModule} from 'ng-zorro-antd/select';
import {NzInputNumberModule} from 'ng-zorro-antd/input-number';
import {NzTableModule} from 'ng-zorro-antd/table';
import { NzBadgeModule } from 'ng-zorro-antd/badge';

import { PlusOutline } from '@ant-design/icons-angular/icons';

import {AngularFontAwesomeModule} from "angular-font-awesome";

import {EditSettingComponent} from "./edit-setting-table/edit.component";
// Import our components
import {EventDBComponent} from "./eventdb.component";
import {StatusComponent} from "./status/status.component";
import {
    TupleActionPushNameService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService
} from "@synerty/vortexjs";

import {
    eventdbActionProcessorName,
    eventdbFilt,
    eventdbObservableName,
    eventdbTupleOfflineServiceName
} from "@peek/peek_plugin_eventdb/_private";
import {EditPropertyComponent} from "./edit-property-table/edit.component";

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
        FormsModule,
        AngularFontAwesomeModule,
        NzTabsModule,
        NzSwitchModule,
        NzButtonModule,
        NzIconModule,
        NzSelectModule,
        NzInputNumberModule,
        NzTableModule,
        NzBadgeModule
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
    declarations: [EventDBComponent, StatusComponent, EditSettingComponent,
        EditPropertyComponent]
})
export class EventDBModule {

}
