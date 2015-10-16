OS: Linux
Browsers: FireFox =>30, Chrome =>30

For install run:
sudo install -r requirements.txt

Create database and superuser:
sudo ./manage.py syncdb

For run test:
sudo make test

For run chat server:
sudo ./run_server.py