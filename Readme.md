# Machine Management API

## Overview

The Machine Management API provides endpoints for managing machines, tools in use, axes, and historical field data. This API supports user registration, JWT authentication, and CRUD operations for various resources.



```
git clone https://github.com/Sinanalungal/machine_management.git
cd machine_management

```

## Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate   # On Mac
venv\Scripts\activate   # On Windows

```

## Install Dependencies

```
pip install -r requirements.txt

```

## Add Env

-> Create .env file :

-> Add these data & and fill the required

```
DB_HOST= your_db_host
DB_USER= your_db_user
DB_PASSWORD= your_db_password
DB_NAME= your_db_name

```

## Apply Migrations


```
python manage.py migrate

```
## Create SuperUser

```
py manage.py createsuperuser
```
give the reuired credentials to the superuser

## Run Application

```
python manage.py runserver
```

## Run Python File

-> Open New Terminal

-> Activate Virtual Environment:

```
source venv/bin/activate   # On Mac
venv\Scripts\activate   # On Windows

```
-> Run Python File Named random_creator.py

```
py random_creator.py

```

## Open Admin panel

```
http://localhost:8000/admin/

```
-give super user credentials to the admin panel and redirect to admin

-open user and click the created user (if you want to create add user and  you have api for that too , but you must set the role through the admin panel)

-assign the role that in the group section to the user


## API Documentation


## User Registration

```
POST http://localhost:8000/register/
```
Description: Register a new user and obtain JWT tokens.
Request Body:json

```
{
  "username": "string",
  "password": "string",
  "confirm_password": "string",
  "email": "string"
}
```
Response:json

```

{
  "refresh": "string",
  "access": "string"
}

```

-user created , but you need to set the role through the admin panel.role setting not included in this registration. otherwise you don't have to access the data


## JWT Token Management

```
POST http://localhost:8000/token/
```
Description: Obtain JWT access and refresh tokens.
Request Body:json

```
{
  "username": "string",
  "password": "string"
}
```
Response:json

```
{
  "refresh": "string",
  "access": "string"
}
```

```
POST http://localhost:8000/token/refresh/
```
Description: Refresh JWT access token using the refresh token.
Request Body:json

```
{
  "refresh": "string"
}
```

Response:json


```
{
  "access": "string"
}
```
## Machine Endpoints

```
GET http://localhost:8000/machines/
```

Description: List all machines.
Response:json

```
[
  {
    "machine_id": "string",
    "machine_name": "string",
    "tool_capacity": "integer",
    "tool_offset": "float",
    "feedrate": "integer",
    "created_at": "string",
    "updated_at": "string"
  }
]
```

```
POST http://localhost:8000/machines/
```
Description: Create a new machine.
Request Body:json

```
{
  "machine_id": "string",
  "machine_name": "string",
  "tool_capacity": "integer",
  "tool_offset": "float",
  "feedrate": "integer"
}
```

Response:json

```
{
  "machine_id": "string",
  "machine_name": "string",
  "tool_capacity": "integer",
  "tool_offset": "float",
  "feedrate": "integer",
  "created_at": "string",
  "updated_at": "string"
}
```

```
GET http://localhost:8000/machines/<str:machine_id>/
```
Description: Retrieve a specific machine by machine_id.
Response: Same format as POST /machines/

```
PUT http://localhost:8000/machines/<str:machine_id>/
```

Description: Update a specific machine by machine_id.
Request Body: 
```
{
    "machine_id": "string",
    "machine_name": "string",
    "tool_capacity": "integer",
    "tool_offset": "float",
    "feedrate": "integer
}
```
Response: Same format as POST /machines/

```
PATCH http://localhost:8000/machines/<str:machine_id>/
```

Description: Partially update a specific machine by machine_id.
Request Body: Any subset of fields from POST /machines/
Response: Same format as POST /machines/

```
DELETE http://localhost:8000/machines/<str:machine_id>/
```

Description: Delete a specific machine by machine_id.
Response: No content.
Tools in Use Endpoints

```
GET http://localhost:8000/toolsinuse/
```

Description: List all tools in use.
Response:json
```
[
  {
    "machine":
        {
            "machine_id": "string",
            "machine_name": "string",
            "tool_capacity": "integer",
            "tool_offset": "float",
            "feedrate": "integer",
            "created_at": "string",
            "updated_at": "string"
        },
    "tool_in_use": "integer",
    "created_at": "string",
    "updated_at": "string"
  }
]
```

```
POST http://localhost:8000/toolsinuse/
```
Description: Create a new tool in use.
Request Body:json

```
{
  "machine": "string",
  "tool_in_use": "integer"
}
```

Response:json

```
{
  "machine": {
            "machine_id": "string",
            "machine_name": "string",
            "tool_capacity": "integer",
            "tool_offset": "float",
            "feedrate": "integer",
            "created_at": "string",
            "updated_at": "string"
        },
  "tool_in_use": "integer",
  "created_at": "string",
  "updated_at": "string"
}
```

```
GET http://localhost:8000/toolsinuse/<str:machine_id>/
```
Description: Retrieve a specific tool in use by machine_id.
Response: Same format as POST /toolsinuse/

```
PUT http://localhost:8000/toolsinuse/<str:machine_id>/
```

Description: Update a specific tool in use by machine_id.
Request Body: Same as POST /toolsinuse/
Response: Same format as POST /toolsinuse/


```
PATCH http://localhost:8000/toolsinuse/<str:machine_id>/
```
Description: Partially update a specific tool in use by machine_id.
Request Body: Any subset of fields from POST /toolsinuse/
Response: Same format as POST /toolsinuse/


```
DELETE http://localhost:8000/toolsinuse/<str:machine_id>/
```
Description: Delete a specific tool in use by machine_id.
Response: No content.
## Axis Endpoints
```
GET http://localhost:8000/axes/<str:machine_id>/
```
Description: List all axes.
Response:json

```
[
  {
    "machine": 
        {
            "machine_id": "string",
            "machine_name": "string",
            "tool_capacity": "integer",
            "tool_offset": "float",
            "feedrate": "integer",
            "created_at": "string",
            "updated_at": "string"
        },
    "axis_name": "string",
    "max_acceleration": "float",
    "max_velocity": "float",
    "actual_position": "float",
    "target_position": "float",
    "homed": "boolean",
    "acceleration": "float",
    "velocity": "float",
    "created_at": "string"
  }
]
```

```
POST http://localhost:8000/axes/<str:machine_id>/
```

Description: Create a new axis.
Request Body:json
```
{
  "axis_name": "string",
  "max_acceleration": "float",
  "max_velocity": "float",
  "actual_position": "float",
  "target_position": "float",
  "homed": "boolean",
  "acceleration": "float",
  "velocity": "float"
}
 
```
Response:json
```
{
  "machine": 
        {
            "machine_id": "string",
            "machine_name": "string",
            "tool_capacity": "integer",
            "tool_offset": "float",
            "feedrate": "integer",
            "created_at": "string",
            "updated_at": "string"
        },
  "axis_name": "string",
  "max_acceleration": "float",
  "max_velocity": "float",
  "actual_position": "float",
  "target_position": "float",
  "homed": "boolean",
  "acceleration": "float",
  "velocity": "float",
  "created_at": "string"
}
```

```
GET http://localhost:8000/axes/<str:machine_id>/<str:axis_name>/
```

Description: Retrieve a specific axis by machine_id and axis_name.
Response: Same format as POST /axes/


```
PUT http://localhost:8000/axes/<str:machine_id>/<str:axis_name>/
```
Description: Update a specific axis by machine_id and axis_name.
Request Body: Same as POST /axes/
Response: Same format as POST /axes/


```
PATCH http://localhost:8000/axes/<str:machine_id>/<str:axis_name>/
```
Description: Partially update a specific axis by machine_id and axis_name.
Request Body: Any subset of fields from POST /axes/
Response: Same format as POST /axes/


```
DELETE http://localhost:8000/axes/<str:machine_id>/<str:axis_name>/
```
Description: Delete a specific axis by machine_id and axis_name.
Response: No content.

## Historical Data Endpoint
```
GET http://localhost:8000/machine/historical-data/
```
*send params in this following:*
-for axis: axis_name="give axis name here"(multiple possible)
-for axis: machine_id="give machine id here"

Description: Retrieve historical data for machines (based on the  latest 15 minutes).
Response:json

```
{
    "machine_tools_in_use": "integer",
    "field_data": [
        {
            "axis": "string",
            "actual_position": "float",
            "target_position": "float",
            "distance_to_go": "float",
            "acceleration": "float",
            "velocity": "float",
            "created_at": "string"
        }
    ]
}

```