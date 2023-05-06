import { Component, OnInit} from '@angular/core';
import { EventsService } from '../../events.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  username: string = '';
  password: string = '';
  loginError: boolean = false;
  constructor(
    private eventsService: EventsService,
    private router: Router
    ){}
  ngOnInit() {
    // const token = localStorage.getItem('token');
    // if (token) {
    //   this.logged = true;
    // }
  }
  login() {
    this.eventsService.login(this.username, this.password).subscribe({
      next: (data) =>{
        localStorage.setItem('token', data.token);
        this.username = '';
        this.password = '';
        this.router.navigate(['/'])
      },
      error: (error) => {
        this.loginError = true;
        window.alert("Your login details are invalid. Please try again.")
      }
    });
  }
}
