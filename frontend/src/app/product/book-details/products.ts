export interface Product{
    id: number;
    name: string;
    author: string;
    price: number;
    img: string;
    description: string;
}
export const products=[
    {
        id: 1,
        name:  'Bulle & Pelle',
        author: 'SAVANNA WALKER',
        price: 16.00,
        img: 'https://auteur.g5plus.net/main/wp-content/uploads/2018/11/product-19-330x462.jpg',
        description: 'Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur erit qui in ea voluptate',
    },
    {
        id: 2,
        name:  'Peter and the Wolf',
        author: 'JOHN WALKER',
        price: 22.00,
        img: 'https://auteur.g5plus.net/main/wp-content/uploads/2018/11/product-06-330x462.jpg',
        description: 'Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur erit qui in ea voluptate',
    },
    {
        id: 3,
        name:  'When the Doves disappeared',
        author: 'HOF NURGIN',
        price: 24.00,
        img: 'https://auteur.g5plus.net/main/wp-content/uploads/2018/11/product-18-330x462.jpg',
        description: 'Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur erit qui in ea voluptate',
    },
    {
        id: 4,
        name:  'The Assault',
        author: 'MESHO BUVAHR, SI MODARSK',
        price: 19.00,
        img: 'https://auteur.g5plus.net/main/wp-content/uploads/2018/11/product-11-330x462.jpg',
        description: 'Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur erit qui in ea voluptate',
    },
]