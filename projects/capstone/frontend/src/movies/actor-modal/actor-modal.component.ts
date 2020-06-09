import { Component, OnInit, Input } from '@angular/core';
import { Movie, MoviesService } from 'src/app/services/movies.service';
import { Cast, CastsService } from 'src/app/services/casts.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-actor-modal',
  templateUrl: './actor-modal.component.html',
  styleUrls: ['./actor-modal.component.scss'],
})
export class ActorModalComponent implements OnInit {

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private movieService: MoviesService,
    private castService: CastsService
    ) { }

  ngOnInit() {  }


  closeModal() {
    this.modalCtrl.dismiss();
  }

}
