import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule} from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {AuthInterceptor} from "./AuthInterceptor";
 
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './top-bar/top-bar.component';
import { BodyComponent } from './pages/body/body.component';
import { BookCategoriesComponent } from './product/book-categories/book-categories.component';
import { RegisterComponent } from './pages/register/register.component';
import { LoginComponent } from './pages/login/login.component';
import { UserAccountComponent } from './pages/account-page/user-account/user-account.component';
import { ContactDetailsComponent } from './pages/account-page/contact-details/contact-details.component';
import { OrdersComponent } from './pages/account-page/orders/orders.component';
import { PaymentComponent } from './pages/account-page/payment/payment.component';
import { BookDetailsComponent } from './product/book-details/book-details.component';
import { BookListComponent } from './product/book-list/book-list.component';
import { CartComponent } from './pages/account-page/cart/cart.component';
import { PageFooterComponent } from './pages/page-footer/page-footer.component';
import { AddressBookComponent } from './pages/account-page/address-book/address-book.component';
import { AccountDashboardComponent } from './pages/account-page/account-dashboard/account-dashboard.component';
// import { LoginPageComponent } from './login-page/login-page.component';

@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    BodyComponent,
    BookCategoriesComponent,
    // BookDetailsComponent,
    // BookListComponent,
    // CategoriesOfCategoryComponent,
    RegisterComponent,
    LoginComponent,
    UserAccountComponent,
    ContactDetailsComponent,
    OrdersComponent,
    PaymentComponent,
    BookDetailsComponent,
    BookListComponent,
    CartComponent,
    PageFooterComponent,
    AddressBookComponent,
    AccountDashboardComponent,
    // LoginPageComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
    // RouterModule.forRoot([
    //   { path: '', component: TopBarComponent},
    //   { path: 'category/:categoryName', component: BookCategoriesComponent },
    //   { path: 'categoryName/:category_name', component: CategoriesOfCategoryComponent},
    // ])
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
