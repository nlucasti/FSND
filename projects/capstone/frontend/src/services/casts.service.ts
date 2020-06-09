import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Cast {
  id: number;
  movie_id: number;
  actor_id:number;
  // cast: Array<{
  //   cast_id:number,
  //   movie_id:number
  // }>;
}

@Injectable({
  providedIn: 'root'
})
export class CastsService {

  url = environment.apiServerUrl;

  public items: {[key: number]: Cast} = {};



  constructor(private auth: AuthService, private http: HttpClient) { }

  // getMovieCast(cast: Cast, movie:Movie) {
  //   if(cast.movie_id == movie.id)
  //   return cast;
  // }
  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getCasts() {
    if (this.auth.can('get:casts')) {
      this.http.get(this.url + '/casts', this.getHeaders())
      .subscribe((res: any) => {
        this.castsToItems(res.casts);
        console.log(res);
      });
    } else {
      this.http.get(this.url + '/casts', this.getHeaders())
      .subscribe((res: any) => {
        this.castsToItems(res.casts);
        console.log(res);
      });
    }

  }

  async saveCast(cast: Cast) {
    if (cast.id >= 0) { // patch
      this.http.patch(this.url + '/casts/' + cast.id, cast, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.castsToItems(res.casts);
        }
      });
    } else { // insert
      const data = await this.http.post(this.url + '/casts', cast, this.getHeaders()).toPromise();
      return data;
    }
}


  deleteCast(cast: Cast) {
    delete this.items[cast.id];
    this.http.delete(this.url + '/casts/' + cast.id, this.getHeaders())
    .subscribe( (res: any) => {

    });
  }

  castsToItems( casts: Array<Cast>) {
    for (const cast of casts) {
      this.items[cast.id] = cast;
    }
  }
}
