U Pitch 🏟️  

A Livescore Application for Universities*  

Tech-U Pitch: A web application for real-time sports competition updates at First Technical University written in Django  


--- Features

-  Live match scores and updates  
-  Support for multiple sports (football, basketball, etc.)  
-  University-focused teams and tournaments  
-  Notifications for ongoing matches (optional future feature)  
-  Mobile-friendly interface  

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** Django Templates / Bootstrap (or specify if you used React, Vue, etc.)  
- **Database:** SQLite (default) / PostgreSQL (recommended for production)  
- **Others:** Django REST Framework (if applicable)  

---

## ⚙️ Installation & Setup

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/u-pitch.git
   cd techupitch
<img width="1063" height="280" alt="image" src="https://github.com/user-attachments/assets/c49965ca-133c-48aa-89fc-0985180e60b9" />

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows


3. Install dependencies
   ```bash
   pip install -r requirements.txt

4. Apply migrations
   ```bash
   python manage.py migrate

5. Create A Superuser
   ```bash
   py manage.py createsuperuser

6. Run The Server
   ```bash
   py manage.py runserver

7. Access the app
   cpp
   http://127.0.0.1:800


---


-- League Table Example

The application automatically calculates:

Matches Played

Wins / Draws / Losses

Goals For & Against

Goal Difference

Points

Position in the table


---


-- Authentication

Users can log in/out using Django’s built-in authentication system.

Admin panel available at /admin/ for managing models (sports, leagues, matches, players, etc.).



---

 
 -- Contributing

Contributions are welcome!

Fork the repo

Create your feature branch (git checkout -b feature-xyz)

Commit changes (git commit -m 'Add feature xyz')

Push to branch (git push origin feature-xyz)

Open a Pull Request
