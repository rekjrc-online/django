# django

To install/run locally using sqllite for database:

1.  git clone https://github.com/rekjrc-online/rekjrc.git
2.  cd rekjrc
3.  pip install -r requirements.txt
4.  copy .env.template to .env
5.  edit .env
6.  provide secret key at least 50 characters
    7a. optionally configure postgres entries in .env
    7b. optionally edit /rekjrc/rekjrc/settings.py
    comment out DATABASES=sqllite block
    uncomment DATABASES=postgres block
7.  migrations.bat ("python manage.py migrate")
8.  run.bat / run.sh ("chmod +x run.sh")
    (runs "python manage.py runserver 0.0.0.0:8000")
9.  browse to http://localhost:8000
