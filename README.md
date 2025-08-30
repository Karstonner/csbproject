# Password Manager
Cyber Security Base Project I
## WARNING
This project contains intentional OWASP Top Ten 2021 vulnerabilities for educational purposes. Never deploy this application in production or use real data!
## Setup
1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run migrations:
```bash
python manage.py migrate
```
4. Create a superuser:
```bash
python manage.py createsuperuser
```
5. Populate test data:
```bash
python manage.py populate_passwords
```
6. Start server:
```bash
python manage.py runserver
```