import { Component, OnInit } from '@angular/core';
import { EventsService } from '../../events.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  name: string = "";
  surname: string = "";
  username: string = "";
  password: string = "";
  email: string = "";
  constructor(
    private eventsService: EventsService,
    private router: Router
    ){}
  ngOnInit(){
  }
  createNewUser(){
    this.eventsService.registration(this.name, this.surname, this.username, this.password, this.email).subscribe((user)=>
    {
      this.name = "";
      this.surname = "";
      this.password = "";
      this.username = "";
      this.email = "";
      this.router.navigate(['/login'])
    })
  }
  }
