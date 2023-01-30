# Mailing service
### Description
This is a service to mail messages to clients. 
Mailing is the process of sending messages to clients.

Clients for mailing are selected on the basis of "tag" and "operator_code" attributes.
You can use API CRUD-operations with Mailing and Client objects.
When you create new mailing object the app selects proper clients, 
using "tag" and "operator_code" attributes. Then the app creates the 
required number of Messages objects in the "ready" status for further sending 
to these clients.

Special script (mailing.py) runs every 10 minutes checks messages that need to be sent and sends it to an external server. 
You can also use two API methods to get statistics on messages sent.

Short API documentation: 
https://documenter.getpostman.com/view/15136042/2s935hST62
### Technologies
Python 3.9,
Django 4.1.5,
Django REST framework 3.14.0.
### Project running in dev-mode.
- Create and active virtual environment
- Install requirements from requirements.txt
```
pip install -r requirements.txt
``` 
- To run API run command in folder with manage.py:
```
python3 manage.py runserver
```
- To start mailing process run command in folder with manage.py:
```
python3 mailing.py
```
### Author
@n1ghtowl

