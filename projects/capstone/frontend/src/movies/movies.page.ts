import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { MoviesService, Movie } from '../services/movies.service';
import { ModalController } from '@ionic/angular';
import { MovieFormComponent } from './movie-form/movie-form.component';
import { ActorModalComponent } from './actor-modal/actor-modal.component';
import {CastsService, Cast} from '../services/casts.service';

@Component({
  selector: 'app-movies',
  templateUrl: 'movies.page.html',
  styleUrls: ['movies.page.scss']
})
export class MoviesPage implements OnInit{
  loginURL: string;
  constructor(public auth: AuthService,public movies: MoviesService,     private modalCtrl: ModalController, public casts: CastsService) {
    this.loginURL = auth.build_login_link('/tabs/movies');
  }

  Object = Object;

  ngOnInit() {
    this.movies.getMovies();
    this.casts.getCasts();
}
  getJoin(cast: Cast, movie: {[key:number]: Movie}) {
    console.log(cast);
    var map= {};
    Object.values(cast).forEach(function(cast) {
      if(map[cast.movie_id]){
        map[cast.movie_id].push(cast);
      }
      else{
        map[cast.movie_id] = [cast];
      }
    });
    // now do the "join":

    Object.values(movie).forEach(function(movie) {
        movie["cast"] = map[movie.id];
    });
    // Object.values(movie).forEach(function(movie) {
    //   this.movies.items[movie.id]= movie
    //     console.log(movie)
    // });
    this.movies.items = movie;
    console.log(this.movies)
    console.log(movie)
  }

  async openForm(activemovie: Movie = null) {
    if (!this.auth.can('get:movies')) {
      return;
    }
  const modal = await this.modalCtrl.create({
    component: MovieFormComponent,
    componentProps: { movie: activemovie, isNew: !activemovie }
  });

  modal.present();
  }

  async openActors(activemovie: Movie = null) {
    if (!this.auth.can('get:movies')) {
      return;
    }
  const modal = await this.modalCtrl.create({
    component: ActorModalComponent,
    componentProps: { movie: activemovie, isNew: !activemovie }
  });

  modal.present();
  }


}
