# Grocery assistant Foodgram.
Available at ip-address http://51.250.13.122/

## Author:
My name is Anton, I am junior backend developer from Saint-Petersburg, Russia.

## Project Description:
This is a site where you can share recipes and culinary secrets with other users, add your own recipes and pictures, make a shopping list, subscribe to people you are interested in.

## Filling .env file:
For the project to work correctly, you need a completed .env file in the / backend / foodgram directory. Example .env file:
> - DB_ENGINE = db
> - DB_NAME = postgres
> - POSTGRES_USER = postgres
> - POSTGRES_PASSWORD = postgres
> - DB_HOST = db
> - DB_PORT = 5432

## Launch of the project:
+ Install Docker
+ Go to the infra / folder in the terminal
+ Run the command: docker-compose up -d --build
+ Go to console of "backend" container, and launch commands "python manage.py makemigrations" and "python manage.py migrate"
+ Launch the site by ip-address