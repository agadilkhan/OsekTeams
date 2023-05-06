import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Category, AuthToken, User, Book, CartItem} from './models'

@Injectable({
  providedIn: 'root'
})
export class EventsService {

  BASE_URL = "http://localhost:8000"

  constructor(private client: HttpClient) { }

  login(username: string, password: string): Observable<AuthToken> {
    return this.client.post<AuthToken>(
      `${this.BASE_URL}/api/login/`,
      {username, password}
    )
  }
  registration(name: string, surname: string, username: string, password: string, email: string): Observable<User>{
    return this.client.post<User>(
      `${this.BASE_URL}/api/registration/`,
        {
          first_name: name,
          last_name: surname,
          username: username,
          password: password,
          email: email
      }
    )
  }
  getCategories(): Observable<Category[]> {
    return this.client.get<Category[]>(
      `${this.BASE_URL}/api/shop/categories/`
    )
  }
  getBooks(): Observable<Book[]>{
    return this.client.get<Book[]>(
      `${this.BASE_URL}/api/shop/books/`
    )
  }
  cartBooks(): Observable<CartItem[]>{
    return this.client.get<CartItem[]>(
      `${this.BASE_URL}/api/cart/books/`
    )
  }
  getCategoryBooks(category_id: number): Observable<Book[]>{
    return this.client.get<Book[]>(
      `${this.BASE_URL}/api/shop/category/${category_id}/books/`
    )
  };
}
