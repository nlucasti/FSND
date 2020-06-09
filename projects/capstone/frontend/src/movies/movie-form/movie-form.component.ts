import { Component, OnInit, Input } from '@angular/core';
import { Movie, MoviesService } from 'src/app/services/movies.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-movie-form',
  templateUrl: './movie-form.component.html',
  styleUrls: ['./movie-form.component.scss'],
})
export class MovieFormComponent implements OnInit {
  @Input() movie: Movie;
  @Input() isNew: boolean;
  @Input() date: string;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private movieService: MoviesService
    ) { }

  ngOnInit() {
    if (this.isNew) {
      var d = new Date()
      this.movie = {
        id: -1,
        title: '',
        release_date: new Date(),
        img_link: 'https://image.flaticon.com/icons/png/512/73/73960.png'
      };
      // this.addIngredient();
    }

  }

  customTrackBy(index: number, obj: any): any {
    return index;
  }
  getIsoDate() {
    var d = new Date(this.movie.release_date);
    this.date =  d.toISOString();
  }
  // addIngredient(i: number = 0) {
  //   this.movie.recipe.splice(i + 1, 0, {name: '', color: 'white', parts: 1});
  // }
  //
  // removeIngredient(i: number) {
  //   this.movie.recipe.splice(i, 1);
  // }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    this.movieService.saveMovie(this.movie);
    this.closeModal();
  }

  deleteClicked() {
    this.movieService.deleteMovie(this.movie);
    this.closeModal();
  }
}
