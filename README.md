# API Documentation

# Login

Used to collect a Token for a registered User.

**URL** : `/api/login/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "username": "[valid email address]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "iloveauth@example.com",
    "password": "abcd1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```

## Error Response

**Condition** : If 'username' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "non_field_errors": [
        "Unable to login with provided credentials."
    ]
}
```

---

# Add City

To add city in DB.

**URL** : `/city/`

**Method** : `POST`

**Auth required** : YES - Admin

**Data constraints**

```json
{
    "name": "[Name of the City]"
}
```

**Data example**

```json
{
    "name": "Ahmedabad"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "id": 10,
    "created_at": "2024-04-22T13:00:01.588654Z",
    "modified_at": "2024-04-22T13:00:01.588654Z",
    "name": "Ahmedabad"
}
```

## Error Response

**Condition** : If 'city' already exists.

**Code** : `204 NO CONTENT`

**Content** :

```json
{
    "message": "City Already exists."
}
```

---

---

# Get City

To add city in DB.

**URL** : `/city/`

**Method** : `GET`

**Auth required** : YES

## Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "id": 1,
        "created_at": "2024-04-15T17:59:14.451044Z",
        "modified_at": "2024-04-15T17:59:14.451044Z",
        "name": "Bangalore"
    },
    {
        "id": 2,
        "created_at": "2024-04-15T17:59:45.554186Z",
        "modified_at": "2024-04-15T17:59:45.554186Z",
        "name": "Chennai"
    }
    
]
```

## Error Response

**Condition** : If user not authorized to use the API.

**Code** : `401 UNAUTHORIZED`

**Content** :

```json
{
    "message": "You do not have access to this API."
}
```

---

# Add Movie

To add movie in DB.

**URL** : `/movie/`

**Method** : `POST`

**Auth required** : YES - Admin

**Data constraints**

```json
{
  "title": "Example Movie",
  "description": "This is an example movie description.",
  "release_date": "YYYY-MM-DD",
  "rating": 8,
  "movieCategory": "ACTION",
  "casts": [1, 2, 3], 
  "languages": [1, 2]  
}
```

Movie Category Enum
```python
class MovieCategory(models.TextChoices):
    ACTION = "ACTION"
    DRAMA = "DRAMA"
    HORROR = "HORROR"
    COMEDY = "COMEDY"
```

**Data example**

```json
{
  "title": "Dunki",
  "description": "A bollywood movie on illegal immigration.",
  "release_date": "2024-04-23",
  "rating": 8,
  "movieCategory": "DRAMA",
  "casts": [2, 3, 4], 
  "languages": [1, 2]  
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "id": 1,
    "created_at": "2024-04-23T11:29:24.318229Z",
    "modified_at": "2024-04-23T11:29:24.318229Z",
    "title": "Dunki",
    "description": "A bollywood movie on illegal immigration.",
    "release_date": "2024-04-23",
    "rating": 8,
    "movieCategory": "DRAMA",
    "casts": [
        2,
        3,
        4
    ],
    "languages": [
        1,
        2
    ]
}
```

## Error Response

**Condition** : If 'movie' already exists.

**Code** : `204 NO CONTENT`

**Content** :

```json
{
    "message": "Movie Already exists."
}
```

---