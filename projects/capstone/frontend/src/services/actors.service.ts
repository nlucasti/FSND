import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Actor {
  id: number;
  name: string;
  age: number;
  gender: string;
  // cast: Array<{
  //   actor_id:number,
  //   movie_id:number
  // }>;
}

@Injectable({
  providedIn: 'root'
})
export class ActorsService {
  url = environment.apiServerUrl;

  public items: {[key: number]: Actor} = {};
  public response: {[key:number]: Actor} = {};
  // actor_id: number;
  constructor(private auth: AuthService, private http: HttpClient) { }

  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getActors() {
    if (this.auth.can('get:actors')) {
      this.http.get(this.url + '/actors', this.getHeaders())
      .subscribe((res: any) => {
        this.actorsToItems(res.actors);
        console.log(res);
      });
    } else {
      this.http.get(this.url + '/actors', this.getHeaders())
      .subscribe((res: any) => {
        this.actorsToItems(res.actors);
        console.log(res);
      });
    }

  }

  async saveActor(actor: Actor, callback = null) {
    if (actor.id >= 0) { // patch
      this.http.patch(this.url + '/actors/' + actor.id, actor, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          // this.actorsToItems(res.actors);

        }
      });
    } else { // insert
      const data = await this.http.post(this.url + '/actors', actor, this.getHeaders()).toPromise();
      this.getResponse(data["actors"]);
      return data;
      // .subscribe( (res: any) => {
      //   this.getResponse(res.actors);
      //   if (res.success) {
      //     // this.actorsToItems(res.actors);
      //   }
      // }).toPromise();
    }

  }
  getResponse(actor: Actor) {
    // this.saveActor(actor)
    this.response = {};
    this.response[actor.id] = actor;
    console.log(this.response)
  }

  deleteActor(actor: Actor) {
    delete this.items[actor.id];
    this.http.delete(this.url + '/actors/' + actor.id, this.getHeaders())
    .subscribe( (res: any) => {

    });
  }

  actorsToItems( actors: Array<Actor>) {
    for (const actor of actors) {
      this.items[actor.id] = actor;
    }
  }
}
