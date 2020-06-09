import { IonicModule } from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MoviesPage } from './movies.page';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

import { MoviesPageRoutingModule } from './movies-routing.module';
import { MovieFormComponent } from './movie-form/movie-form.component';
import { ActorModalComponent } from './actor-modal/actor-modal.component';
@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    MoviesPageRoutingModule
  ],
  entryComponents: [MovieFormComponent, ActorModalComponent],
  declarations: [MoviesPage, MovieFormComponent, ActorModalComponent]
})
export class MoviesPageModule {}
