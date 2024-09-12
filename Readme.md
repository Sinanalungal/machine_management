# Machine Management API

## Overview

The Machine Management API provides endpoints for managing machines, tools in use, axes, and historical field data. This API supports user registration, JWT authentication, and CRUD operations for various resources.



```
git clone https://github.com/yourusername/machine-management-api.git
cd machine-management-api
```

## Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate   # On Mac
`venv\Scripts\activate`   # On Windows

```

## Install Dependencies

```
pip install -r requirements.txt
```

## Apply Migrations


```
python manage.py migrate
python manage.py runserver
```

```
python manage.py runserver
```

## API Documentation


## User Registration

```
POST /register/
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

## JWT Token Management

```
POST /token/
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
POST /token/refresh/
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
GET /machines/
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
POST /machines/
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
GET /machines/<str:machine_id>/
```
Description: Retrieve a specific machine by machine_id.
Response: Same format as POST /machines/

```
PUT /machines/<str:machine_id>/
```

Description: Update a specific machine by machine_id.
Request Body: Same as POST /machines/
Response: Same format as POST /machines/

```
PATCH /machines/<str:machine_id>/
```

Description: Partially update a specific machine by machine_id.
Request Body: Any subset of fields from POST /machines/
Response: Same format as POST /machines/

```
DELETE /machines/<str:machine_id>/
```

Description: Delete a specific machine by machine_id.
Response: No content.
Tools in Use Endpoints

```
GET /toolsinuse/
```

Description: List all tools in use.
Response:json
```
[
  {
    "machine": "string",
    "tool_in_use": "integer",
    "created_at": "string",
    "updated_at": "string"
  }
]
```

```
POST /toolsinuse/
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
  "machine": "string",
  "tool_in_use": "integer",
  "created_at": "string",
  "updated_at": "string"
}
```

```
GET /toolsinuse/<str:machine_id>/
```
Description: Retrieve a specific tool in use by machine_id.
Response: Same format as POST /toolsinuse/

```
PUT /toolsinuse/<str:machine_id>/
```

Description: Update a specific tool in use by machine_id.
Request Body: Same as POST /toolsinuse/
Response: Same format as POST /toolsinuse/


```
PATCH /toolsinuse/<str:machine_id>/
```
Description: Partially update a specific tool in use by machine_id.
Request Body: Any subset of fields from POST /toolsinuse/
Response: Same format as POST /toolsinuse/


```
DELETE /toolsinuse/<str:machine_id>/
```
Description: Delete a specific tool in use by machine_id.
Response: No content.
## Axis Endpoints
```
GET /axes/
```
Description: List all axes.
Response:json

```
[
  {
    "machine": "string",
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
POST /axes/
```

Description: Create a new axis.
Request Body:json
```
{
  "machine": "string",
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
  "machine": "string",
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
GET /axes/<str:machine_id>/<str:axis_name>/
```

Description: Retrieve a specific axis by machine_id and axis_name.
Response: Same format as POST /axes/


```
PUT /axes/<str:machine_id>/<str:axis_name>/
```
Description: Update a specific axis by machine_id and axis_name.
Request Body: Same as POST /axes/
Response: Same format as POST /axes/


```
PATCH /axes/<str:machine_id>/<str:axis_name>/
```
Description: Partially update a specific axis by machine_id and axis_name.
Request Body: Any subset of fields from POST /axes/
Response: Same format as POST /axes/


```
DELETE /axes/<str:machine_id>/<str:axis_name>/
```
Description: Delete a specific axis by machine_id and axis_name.
Response: No content.

## Historical Data Endpoint
```
GET /machine/historical-data/
```
Description: Retrieve historical data for machines.
Response:json

```
    [
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

```