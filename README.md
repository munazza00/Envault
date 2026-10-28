 ENVAULT – Team Environment Variable Manager

ENVAULT is a secure, Django-based web application that helps teams manage environment variables across multiple projects and environments. It provides centralized storage, encrypted handling of sensitive values, access control, variable history, and convenient `.env` file imports.

 Features

- *User Authentication:* Secure signup, login, and logout.
- *Project Management:* Create and manage projects.
- *Team Collaboration:* Add registered users to projects.
- *Multiple Environments:* Organize variables into Development, Staging, and Production.
- *Variable Management:* Create, edit, delete, and classify environment variables as Standard or Sensitive.
- *Secure Storage:* Sensitive values are encrypted before being stored in the database.
- *Controlled Secret Reveal:* Sensitive values are masked by default. Only project owners and members with reveal permission can view them.
- *
*Variable History:* Track variable creation, updates, classification changes, and deletion, including the actor and timestamp.
- *Smart `.env` Import:* Paste environment variable entries, preview changes, and identify New, Update, and Unchanged variables before importing.
- *Responsive Interface:* Built with Bootstrap 5.

 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| PostgreSQL | Database |
| Bootstrap 5 | Frontend styling |
| Django Templates | User interface |
| HTMX | Dynamic interactions |
| Pydantic | Data validation |
| Cryptography (Fernet) | Sensitive value encryption |
| Argon2 | Password hashing |
| django-environ | Environment configuration |

 Project Structure

```text
ENVAULT/
│
├── accounts/          # User authentication
├── projects/          # Project and membership management
├── environments/      # Project environments
├── variables/         # Variable management, encryption and history
├── envault/            # Main Django configuration
│
├── manage.py
├── requirements.txt
├── .env                # Private configuration (not committed)
├── .gitignore
└── README.md
```

 Getting Started

 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ENVAULT
```

 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

 3. Install dependencies

```bash
pip install -r requirements.txt
```

 4. Configure environment variables

Create a `.env` file in the project root and configure the required settings, including:

- Django secret key
- Database name, username, password, host, and port
- Fernet encryption key
- Debug and allowed-host settings

Never commit `.env` or expose encryption keys and database credentials.

5. Set up the database

Make sure PostgreSQL is running and the configured database exists.

Run:

'''bash
python manage.py migration

 6. Create an administrator account

```bash
python manage.py createsuperuser
```

 7. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

 Security

ENVAULT is designed with security as a core consideration:

- Passwords are stored using secure password hashing.
- Sensitive environment variable values are encrypted using Fernet.
- Sensitive values are masked in the interface by default.
- Secret reveal access is controlled separately from project membership.
- Variable history records actions without storing plaintext secret values.
- Private configuration is kept outside the source code.

 Future Improvements

- Email-based project invitations.
- More granular project permissions.
- Automated deployment and production monitoring.
- Additional audit and security controls.

 Author

Developed as a Python and Django course final project.

---

ENVAULT – Secure Environment Variable Management for Teams.