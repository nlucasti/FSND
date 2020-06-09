import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActorsPage } from './actors.page';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

import { ActorsPageRoutingModule } from './actors-routing.module';
import { ActorFormComponent } from './actor-form/actor-form.component';
@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    ActorsPageRoutingModule
  ],
  entryComponents: [ActorFormComponent],
  declarations: [ActorsPage, ActorFormComponent]
})
export class ActorsPageModule {}
