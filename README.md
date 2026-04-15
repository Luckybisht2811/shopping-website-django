# 🛒 ShoppingLyx — Full-Stack Django eCommerce Website

**A modern online shopping platform with Razorpay payment integration.**  

🔗 **Live Demo:** [Visit Lucky-Store](https://lucky-store-kgh4.onrender.com)

---

## 📌 Overview

**ShoppingLyx** is a full-stack **eCommerce website** built with **Django, Python, HTML/CSS/JS**.  
Users can browse products, add them to the cart, and pay via **Cash on Delivery (COD)** or **Razorpay Online Payment**.  
Admins can manage products and track orders seamlessly.  

This project demonstrates **full-stack development, database management, and payment gateway integration** — perfect for your portfolio.  

---

## 🚀 Features

### 💻 User Features
- User registration & secure login
- Browse products by categories: **Topwear, Bottomwear, Earrings, Necklaces**
- Add to Cart & **Buy Now**
- Multiple addresses during checkout
- Payment options:
  - **Cash on Delivery (COD)**
  - **Razorpay Online Payment**
- View order history and order details

### ⚙️ Admin Features
- Manage products (Add/Edit/Delete)
- View all orders and payment status
- Dashboard for easy order tracking

### 🛠 Technical Features
- Backend: **Django 6.x**, **Python 3.12**
- Frontend: **HTML5, CSS3, Bootstrap 5, JavaScript**
- Payment Integration: **Razorpay API**
- Database: **SQLite** (switchable to MySQL/PostgreSQL)
- Responsive design for mobile & desktop
- Secure login & CSRF protection

  ### 👨‍💻 Author

  Lalit Singh Bisht
  Email: lalitsinghbisht@example.com

  ### 📝 License
This project is open-source and free for learning & portfolio purposes.


---

## 📂 Project Structure

```text
shoppinglyx/
│
├─ app/                  # Main Django app
│  ├─ migrations/        # Database migrations
│  ├─ static/app/        # CSS, JS, Images
│  ├─ templates/app/     # HTML templates
│  ├─ models.py          # Database models
│  ├─ views.py           # Application views
│  └─ urls.py            # App URLs
│
├─ manage.py             # Django project runner
├─ shoppinglyx/          # Project settings
├─ requirements.txt      # Python dependencies
└─ .gitignore            # Git ignore file

## ⚡ Installation & Setup
### 📂 Technologies Used
Backend: Django, Python
Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
Database: SQLite (default), compatible with MySQL/PostgreSQL
Payment Gateway: Razorpay API
Version Control: Git & GitHub

## ⚡ Installation & Setup

1. **Clone the repository**
git clone https://github.com/Luckybisht2811/shopping-website-django.git
cd shopping-website-django
Install dependencies

pip install -r requirements.txt
Apply migrations

python manage.py makemigrations
python manage.py migrate
Create superuser for admin

python manage.py createsuperuser
Run the development server

python manage.py runserver
Open the project in your browser: http://127.0.0.1:8000/


