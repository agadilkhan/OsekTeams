import { Component, OnInit } from '@angular/core';
import { Category, Book }  from '../../models';
import { EventsService } from '../../events.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-book-categories',
  templateUrl: './book-categories.component.html',
  styleUrls: ['./book-categories.component.css']
})
export class BookCategoriesComponent implements OnInit{
  categories: Category[] = [];
  books: Book[] = [];
  // category: Category;

  // newCategory: string = "";
  constructor(private eventsService: EventsService,){
    }

  ngOnInit(){
    this.eventsService.getCategories().subscribe((categories) => 
      {
        this.categories = categories;
        console.log(this.categories)
      });
  }
  // getCategoryBooks(category_id:number){
  //   this.eventsService.getCategoryBooks(category_id).subscribe((books)=>{

  //   })
  // }
}





// createNewCategory(){
  //   this.eventsService.createCategory(this.newCategory).subscribe((category) => 
  //   {
  //     this.categories.push(category); 
  //     this.newCategory= "";
  //     console.log(this.categories);
  //   });
  // }
  // deleteCategory(category_id: number) {
  //   console.log(category_id)
  //   this.eventsService.deleteCategory(category_id).subscribe((item) => 
  //   {
  //     this.categories = this.categories.filter((category) => category.id !== category_id);
  //   });
  // }