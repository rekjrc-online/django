# django

To install/run locally using sqllite for database:

1.  git clone https://github.com/rekjrc-online/rekjrc.git
2.  cd rekjrc
3.  pip install -r requirements.txt
4.  copy .env.template to .env
5.  edit .env
6.  provide secret key at least 50 characters
7.  configure postgres db fields in .env
8.  edit /rekjrc/rekjrc/settings.py
    comment out either the sqllite block or the postgres block
9.  "migrate.bat" ("python manage.py migrate")
    or "migrate.sh" ("chmod +x migrate.sh")
10. runserver.bat / runserver.sh ("chmod +x runserver.sh")
    (runs "python manage.py runserver")
11. browse to http://localhost:8000
