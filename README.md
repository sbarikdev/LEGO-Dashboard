
## Backend
Follow the steps to run this project:

1. git clone https://github.com/sbarikdev/LEGO-Web.git

2. cd LEGO-Web

3. python -m venv venv

4. source venv/bin/activate (for linux/macOS user)
   
4. \venv\Scripts\activate.bat (for windows user)

5. pip install -r requirements.txt

6. python manage.py runserver

then run http://localhost:8000 on your browser.


## Docker:
sudo chown $USER /var/run/docker.sock
docker-compose build
docker-compose up

## celery: 
celery -A core worker -l info