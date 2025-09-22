# 🐾 Paws & Whiskers – Animal Shelter Web App

A Django-based web application for managing and showcasing adoptable animals at an animal shelter.  
Built with **Django**, **PostgreSQL**, **Bootstrap 5**, and **Crispy Forms**.

---

## 🚀 Features

- 🔐 **User Authentication** (signup, login, logout)  
- 📋 **Animal Management**
  - List all animals available for adoption
  - Filter by animal type
  - View detailed animal profiles
- 📱 **Responsive Design** with Bootstrap 5
- 🌍 **International Phone Input** with country codes
- 🖼️ Upload **animal photos** and **user profile photos**
- 🏠 Landing page with featured animals
- 🧩 Extendable structure for future adoption workflows

---


## 🛠️ Tech Stack

- **Backend:** Django 5, Python 3.13  
- **Database:** PostgreSQL  
- **Frontend:** Bootstrap 5 + Crispy Forms + custom CSS  
- **Auth:** Django’s built-in authentication system  
- **Media Handling:** Django file uploads for photos  

---

## ⚙️ Installation & Setup

1. **Clone the repository**  
   ```sh
   git clone <repo-url>
   cd animal_shelter
   ```

2. **Create and activate a virtual environment**  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**  
   - Copy `.env.example` to `.env` and set your database credentials and secret key.

5. **Apply migrations**  
   ```sh
   python manage.py migrate
   ```

6. **Create a superuser**  
   ```sh
   python manage.py createsuperuser
   ```

7. **Run the development server**  
   ```sh
   python manage.py runserver
   ```

8. **Access the app**  
   - Visit [http://localhost:8000/](http://localhost:8000/) in your browser.


📂 Project Structure
csharp
Copy code
animal_shelter/
├── shelter/               # Main app
│   ├── models.py          # Animal & User models
│   ├── views.py           # App views
│   ├── urls.py            # URL routes
│   ├── templates/         # HTML templates
│   └── static/            # Static files (CSS, JS, images)
├── shelter_project/       # Project settings
├── media/                 # Uploaded media files
├── static/                # Global static assets
├── requirements.txt
└── README.md

🧩 Roadmap

✅ User authentication (signup/login/logout)

✅ Animal list & detail pages

✅ Filtering by animal type

🚧 Adoption application form

🚧 Admin dashboard for managing animals

🚧 Email notifications for adoption requests

🤝 Contributing
Pull requests are welcome!

Fork the repo

Create a new branch (feature/your-feature)

Commit your changes

Open a PR 🚀

📜 License
This project is licensed under the MIT License – feel free to use and modify.

