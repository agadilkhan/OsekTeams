export interface Category{
    id: number;
    name: string;
}

export interface Book{
    id: number;
    name: string;
    author: string;
    description: string;
    image: string;
    image_url: string;
    price: number;
    category: number;
}

export interface AuthToken{
    token: string;
}
export interface User{
    name: string;
    surname: string;
    email: string;
    username: string;
    password: string;
}

export interface CartItem{
    book: Book;
    quantity: number;
}