import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {Routes} from "@angular/router";
import {NzDropDownModule} from 'ng-zorro-antd/dropdown';
import {AngularFontAwesomeModule} from "angular-font-awesome";
import {NzTableModule} from 'ng-zorro-antd/table';
import {NzToolTipModule} from 'ng-zorro-antd/tooltip';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzCardModule} from 'ng-zorro-antd/card';
import {NzMenuModule} from 'ng-zorro-antd/menu';
import {NzModalModule} from 'ng-zorro-antd/modal';
import {EventDBEventListComponent} from "./event-list-component/event-list.component";
import {EventDBPageComponent} from "./event-page-component/event-page.component";

// Import a small abstraction library to switch between nativescript and web
import {PeekModuleFactory} from "@synerty/peek-util-web";



// Define the child routes for this plugin
export const pluginRoutes: Routes = [
    {
        path: '',
        pathMatch: 'full',
        component: EventDBPageComponent
    }
];

@NgModule({
    imports: [
        CommonModule,
        PeekModuleFactory.RouterModule,
        PeekModuleFactory.RouterModule.forChild(pluginRoutes),
        NzDropDownModule,
        NzTableModule,
        NzToolTipModule,
        NzButtonModule,
        NzCardModule,
        NzMenuModule,
        NzModalModule,
        AngularFontAwesomeModule
    ],
    exports: [EventDBEventListComponent],
    providers: [],
    declarations: [EventDBPageComponent, EventDBEventListComponent]
})
export class EventDBModule {
}
