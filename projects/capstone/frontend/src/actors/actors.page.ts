import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { ActorsService, Actor } from '../services/actors.service';
import { ModalController } from '@ionic/angular';
import { ActorFormComponent } from './actor-form/actor-form.component';

@Component({
  selector: 'app-actors',
  templateUrl: 'actors.page.html',
  styleUrls: ['actors.page.scss']
})
export class ActorsPage implements OnInit{
  loginURL: string;
  constructor(public auth: AuthService,public actors: ActorsService,     private modalCtrl: ModalController
) {
    this.loginURL = auth.build_login_link('/tabs/actors');
  }

  Object = Object;

  ngOnInit() { this.actors.getActors(); }

  async openForm(activeactor: Actor = null) {
    if (!this.auth.can('get:actors')) {
      return;
    }
  const modal = await this.modalCtrl.create({
    component: ActorFormComponent,
    componentProps: { actor: activeactor, isNew: !activeactor }
  });

  modal.present();
  }


}
