# Praylink
A service that allows people to text in a prayer request.

## About
Came about as a way to gather prayer requests for a youth ministry.

## Features
Prayer requests are added to Google Spreadsheet, and if it's an "urgent" prayer it will also be sent to a GroupMe group. There is also a website where people can pray for prayer requests and create an account to get updates on the prayers they have prayed for. Admin functionality is available to edit and delete prayers.

## Installation
Praylink uses the Flask web framework, meaning that Python(3.6+) needs to be installed. It also uses celery for regular and periodic tasks, but it is not necessary for development unless certain features need to be tested.

Recently, the project has been "Dockerized" making it more easy to develop and for more people to get involved.

1. Change `settings.py.example` into `settings.py` and configure it
2. Get a `client_secret.json` file from Google API Developer Console for Google Sheets, and put that in the `/praylink` folder
3. Run `docker-compose up --build`
4. Run `docker-compose exec web python manage.py init`
5. Run `docker-compose exec web python manage.py migrate`
6. Run `docker-compose exec web python manage.py upgrade`
7. Develop! (Or whatever)

As of right now, to sign-up you need to text the number. The first person to sign-up is admin, as of right now.