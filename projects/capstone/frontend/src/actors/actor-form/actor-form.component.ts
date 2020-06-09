import { Component, OnInit, Input } from '@angular/core';
import { Actor, ActorsService } from 'src/app/services/actors.service';
import { Movie, MoviesService} from 'src/app/services/movies.service';
import { Cast, CastsService} from 'src/app/services/casts.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-actor-form',
  templateUrl: './actor-form.component.html',
  styleUrls: ['./actor-form.component.scss'],
})

export class ActorFormComponent implements OnInit {
  @Input() actor: Actor;
  @Input() cast: Cast;
  @Input() isNew: boolean;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    public actorService: ActorsService,
    private castService: CastsService,
    public movies: MoviesService
    ) { }


  ngOnInit() {
    if (this.isNew) {
      this.actor = {
        id: -1,
        name: '',
        age: 0,
        gender: ''      };
      // this.movies = {};
      // this.addIngredient();
    }
   if (!this.cast) {
      this.cast = {
        id: -1,
        movie_id: -9,
        actor_id: -9
      };
   }
    this.movies.getMovies();
  }
  Object = Object;

  customTrackBy(index: number, obj: any): any {
    return index;
  }

  // addIngredient(i: number = 0) {
  //   this.actor.recipe.splice(i + 1, 0, {name: '', color: 'white', parts: 1});
  // }
  //
  // removeIngredient(i: number) {
  //   this.actor.recipe.splice(i, 1);
  // }
  public testFunc(): void{
    console.log(this.cast)
  }
  closeModal() {
    this.modalCtrl.dismiss();
  }

async saveClicked() {
    this.closeModal();
    var promise = await this.actorService.saveActor(this.actor);
    console.log(this.cast.actor_id)
    if(this.cast.movie_id != -9){
    // this.actorService.getResponse(this.actorService.response)
      console.log(this.actorService.response);
      if(!this.cast.actor_id || this.cast.actor_id == -1){
        this.cast.actor_id = parseInt(Object.keys(this.actorService.response)[0]);
      }
      promise = this.castService.saveCast(this.cast);
      this.testFunc();
    };
  }

  deleteClicked() {
    this.actorService.deleteActor(this.actor);
    this.closeModal();
  }
  getCastID(actor: Actor){
    this.cast.actor_id = actor.id;
    console.log(this.cast)
  }

}
