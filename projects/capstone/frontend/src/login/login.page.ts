import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: 'login.page.html',
  styleUrls: ['login.page.scss'],
})
export class LoginPage implements OnInit {
  loginURL: string;
  token: string;
  constructor(public auth: AuthService) {
    this.loginURL = auth.build_login_link('');
    this.token = auth.activeJWT();
  }

  ngOnInit() {
  }

}
