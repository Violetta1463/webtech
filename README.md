py -m venv venv
venv\Scripts\activate.bat
pip install django==5.0.7
cd webtech
django-admin startproject webtech .
python manage.py runserver
python manage.py startapp pages
mkdir -p templates\pages
mkdir static
