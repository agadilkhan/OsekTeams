import { Component, OnInit } from '@angular/core';
import { EventsService } from '../../../events.service';
import { CartItem } from '../../../models' 

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit{
  items: CartItem[] = []
  constructor(private eventService: EventsService){}

  ngOnInit(){
    this.eventService.cartBooks().subscribe((books)=>{
      this.items = books;
    })
  }
}
