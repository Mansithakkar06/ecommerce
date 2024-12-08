# HandmadeCharm - Handicraft E-Commerce Website
HandmadeCharm is a fully functional e-commerce website designed to connect artisans and users, offering a platform to buy and sell unique handicraft items. The project includes dedicated user and seller functionalities, ensuring a seamless experience for both parties.

__________________

## Features
### User Side
* *User Registration & Login*: Secure authentication system for users.
* *Browse Products*: View a variety of handicraft items uploaded by sellers.
* *Add to Cart*: Add desired products to the shopping cart.
* *lace Orders*: Complete purchases with a streamlined ordering system.
* *Like Products*: Mark favorite items for quick access.
* *Make Payments*: Secure payment gateway for transactions.
* *Order History*: Access past orders and their details.

### Seller Side
* *Seller Registration & Login*: Secure authentication for sellers.
* *Add Products*: Upload products with images, descriptions, and pricing.
* *Update Products*: Edit product details as needed.
* *Delete Products*: Remove products from the catalog.
* *View Orders*: Manage and track user orders.

__________________

## Technologies Used
#### Frontend
* *HTML5*
* *CSS3*
* *Bootstrap*: For responsive design and styling.
* *JavaScript*: For interactivity.

#### Backend
* *Python Django*: A powerful backend framework.

#### Database
* *SQLite*: Django's inbuilt lightweight database.

__________________

## Project Setup
### Prerequisites
* Python (3.10 or later recommended)
* Virtual Environment (venv)
* Git

### Installation Steps
#### 1.Clone the Repository:
```bash
git clone https://github.com/Mansithakkar06/ecommerce.git
cd ecomm
```

#### 2.Set Up Virtual Environment:
```bash
python -m venv env
source env/bin/activate  # For Linux/Mac
env\Scripts\activate     # For Windows
```

#### 3.Install Requirements:
```bash
pip install -r requirements.txt
```

#### 4.Set Up the Database:
* Apply migrations to initialize the SQLite database.
```bash
python manage.py migrate
```

#### 5.Run the Server:
```bash
python manage.py runserver
```

#### 6.Access the Website: 
Open your browser and navigate to http://127.0.0.1:8000.

__________________

## Usage

#### 1.Users:
* Register or log in to explore the product catalog.
* Add products to the cart and proceed with secure payment.
* Like products to save them for later.
* View order history at any time.

#### 2.Sellers:
* Register or log in as a seller.
* Add, update, or delete products.
* Manage orders placed by users.

__________________

## Project Structure
```bash
ecommerce/
│
├── ecomm/               # Project settings and configuration (views, models, etc.)
│
├── templates/           # HTML templates
│   ├── user/            # User-related templates
│   └── seller/          # Seller-related templates
│
├── db.sqlite3           # SQLite database
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```
