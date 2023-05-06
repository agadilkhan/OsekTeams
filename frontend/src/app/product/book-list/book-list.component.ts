import { Component, OnInit, Input } from '@angular/core';
import { Book } from '../../models';
import { EventsService } from '../../events.service';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-book-list',
  templateUrl: './book-list.component.html',
  styleUrls: ['./book-list.component.css']
})
export class BookListComponent implements OnInit{
  // @Input() book !: Book[];
  books: Book[] = []

  constructor(private eventsService: EventsService,
              private activateRoute: ActivatedRoute){}
  ngOnInit(){
    this.eventsService.getBooks().subscribe((books) => 
    {
      this.books = books;
      console.log(this.books)
    });
  }

  share() {
    window.alert('The product has been shared!');
  }

  onNotify() {
    window.alert('You will be notified when the product goes on sale');
  }
}

