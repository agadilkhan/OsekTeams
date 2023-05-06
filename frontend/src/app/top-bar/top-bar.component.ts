import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})
export class TopBarComponent{
  logged: boolean = false;
  ngOnInit() {
    console.log(this.logged)
    const token = localStorage.getItem('token');
    if (token) {
      this.logged = true;
    }
  }
  logout() {
    localStorage.removeItem('token');
    // Request to the Django
    this.logged = false;
  }
}
