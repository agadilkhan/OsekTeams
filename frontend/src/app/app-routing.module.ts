import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BodyComponent } from './pages/body/body.component';
import { RegisterComponent } from './pages/register/register.component';
import { LoginComponent } from './pages/login/login.component';
import { TopBarComponent } from './top-bar/top-bar.component';
import { BookCategoriesComponent } from './product/book-categories/book-categories.component';
import { UserAccountComponent } from './pages/account-page/user-account/user-account.component';
import { ContactDetailsComponent } from './pages/account-page/contact-details/contact-details.component';
import { OrdersComponent } from './pages/account-page/orders/orders.component';
import { BookDetailsComponent } from './product/book-details/book-details.component';
import { BookListComponent } from './product/book-list/book-list.component';
import { PaymentComponent } from './pages/account-page/payment/payment.component';
import { CartComponent } from './pages/account-page/cart/cart.component';
import { AddressBookComponent } from './pages/account-page/address-book/address-book.component';
// import { CategoriesOfCategoryComponent } from './categories-of-category/categories-of-category.component';

const routes: Routes = [
    { path: '', component: BodyComponent},
    { path: 'login', component: LoginComponent},
    { path: 'register', component: RegisterComponent},
    { path: 'category/:id', component: BookCategoriesComponent },
    { path: 'products/:categoryId', component: BookListComponent},
    { path: 'book', component: BookDetailsComponent},
    { path: 'account', component: UserAccountComponent},
    { path: 'contact_details', component: ContactDetailsComponent},
    { path: 'orders', component: OrdersComponent},
    { path: 'payment', component: PaymentComponent},
    { path: 'cart', component: CartComponent},
    { path: 'address', component: AddressBookComponent},
    // { path: 'categoryName/:category_name', component: CategoriesOfCategoryComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
