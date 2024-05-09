# BookMyShow Django Project
___
This project is made to practice low level design, algorithms and ofcourse django framework.

## Problem Statement
___
- An event ticket booking system to book seats for movies, theaters, and stadiums.
- The project has to have a class diagram, schema diagram, and machine coding.
- It has to be a backend server only for now.
- The data has to persist in the Database.
- The project should have API routes, not just MVC.
- For now, no need to connect to third-party APIs, keep it a dummy functionality

## Requirements
___
- There will be 4 user types: customer, event organizer, event manager, and admin. Each user has its own set of controls.
- The customer can:
    - Search for events over the app, can filter by event type (movie, theater, match)
    - It can select an event and check its details such as type, title, casts, date, time, seat map, location, seat-wise cost, and minimum cost.
    - Book a ticket, for multiple people, make payments, create tickets, and manage observer.
    - Option to cancel the ticket and manage the observer.
- The event organizer can:
    - Create an event in the app; adding type, title, seating plan, seat-wise cost, date, time, payment account, and event managers
- The event manager can:
    - Verify customer in the event.
- The admin can:
    - Can edit or add on behalf of customers and organizers.
- Movies and acts can have the same theater structure whereas match happens in stadiums.

## Use Case Diagram
___
![Use case Diagram](media/BMS_usecase_diagram.jpeg)

## Commands to Run
- Make sure you have python 3.12.x and MySQL installed in your system.
- Open terminal and clone the repository `git clone https://github.com/mazumdarsoubhik/BookMyShow-Django-Backend.git`
- Navigate to the repository `cd BookMyShow-Django-Backend`
- Make migrations to manage DB:
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- Run server `python manage.py runserver`

## API Documentation
___

List of Admin APIs:
- [ADD City](#add-city)
- [ADD Casts](#add-casts)
- [ADD Movie](#add-movie)
- [ADD Movie Theater](#add-movie-theater)

List of Organizer APIs:
- [ADD Movie Screen](#add-movie-screen)
- [ADD Movie Seats](#add-movie-seats)
- [ADD Movie Show](#add-movie-show)
- [ADD Movie Show Screen](#add-movie-show-screen)

List of Manager APIs:
- [Verify Ticket](#verify-ticket)

List of Customer APIs:

[//]: # (- [GET City]&#40;#get-city&#41;)

[//]: # (- [GET Casts]&#40;#get-casts&#41;)

[//]: # (- [GET Movie]&#40;#get-movie&#41;)

[//]: # (- [GET Movie Theater]&#40;#get-movie-theater&#41;)

[//]: # (- [GET Movie Screen]&#40;#get-movie-screen&#41;)

[//]: # (- [GET Movie Show]&#40;#get-movie-show&#41;)
- [Search Movies](#search-movies)
- [Search Movie Screen](#search-movies-screen)
- [Search Movie Seat](#search-movies-seat)
- [Book Movie](#book-movie)

List of APIs for Third Party:
- [Payment Confirmation](#payment-confirmation)


# Add City

To add city in DB.

**URL** : `/city`

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

**Code** : `201 CREATED`

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

# Get City

To get list of cities from DB.

**URL** : `/city`

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

# Add Casts

To add cast (Actors) in DB.

**URL** : `/casts`

**Method** : `POST`

**Auth required** : YES - Admin

**Data constraints**

```json
{
    "name": "[Name of the Cast]"
}
```

**Data example**

```json
{
    "name": "Sharman Joshi"
}
```

## Success Response

**Code** : `201 Created`

**Content example**

```json
{
    "id": 8,
    "created_at": "2024-04-26T13:13:46.702809Z",
    "modified_at": "2024-04-26T13:13:46.702809Z",
    "name": "Sharman Joshi"
}
```

## Error Response

**Condition** : If cast already present in DB.

**Code** : `201 CREATED`

**Content** :

```json
{
  "message": "Movie cast already exists"
}
```

# Get Casts

To get list of all the casts from DB.

**URL** : `/casts`

**Method** : `GET`

**Auth required** : YES - Admin

## Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "id": 1,
        "created_at": "2024-04-23T11:21:03.992438Z",
        "modified_at": "2024-04-23T11:21:03.992438Z",
        "name": "Deepika Padukone"
    },
    {
        "id": 2,
        "created_at": "2024-04-23T11:21:23.626952Z",
        "modified_at": "2024-04-23T11:21:23.627984Z",
        "name": "Shahrukh Khan"
    }
    
]
```

## Error Response

**Condition** : If cast already present in DB.

**Code** : `201 CREATED`

**Content** :

```json
{
  "message": "Movie cast already exists"
}
```

# Add Movie

To add a movie in DB.

**URL** : `/movie`

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

**Code** : `201 CREATED`

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

# Get Movie

To get list of movies from DB.

**URL** : `/movie`

**Method** : `GET`

**Auth required** : YES - Admin

## Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "id": 2,
        "created_at": "2024-04-26T13:15:41.149158Z",
        "modified_at": "2024-04-26T13:15:41.149158Z",
        "title": "3 idiots",
        "description": "A bollywood comedy movie on education system.",
        "release_date": "2009-12-02",
        "rating": 9.0,
        "movieCategory": "COMEDY",
        "duration": 120,
        "casts": [
            5,
            6,
            7,
            8
        ],
        "languages": [
            2
        ]
    }
]
    
]
```

# Add Movie Theater

To add movie theater in DB upon registration of organizer of the theater.

**URL** : `/movie/theater`

**Method** : `POST`

**Auth required** : YES - Admin

**Data constraints**

```json
{
    "eventType": ["Type of event"],
    "name": ["Name of the Theater"],
    "city": ["City ID"],
    "organizer": ["organizer ID"]
}
```

Event Type Enum
```python
class EventType(models.TextChoices):
    CINEMA = "CINEMA"
    ACT = "ACT"
    STADIUM = "STADIUM"
```

**Data example**

```json
{
    "eventType": "CINEMA",
    "name": "PVR, Lulu Mall",
    "city": 3,
    "organizer": 1
}
```

## Success Response

**Code** : `201 CREATED`

**Content example**

```json
{
    "id": 1,
    "created_at": "2024-04-23T12:30:57.788553Z",
    "modified_at": "2024-04-23T12:30:57.788553Z",
    "eventType": "CINEMA",
    "name": "PVR, Park Square Mall",
    "city": 1,
    "organizer": 1
}
```

# Get Movie Theater

# Add Movie Screen

# Get Movie Screen

# Add Movie Seats

# Add Movie Show

# Get Movie Show

# Add Movie Show Screen

# Search Movies

# Search Movies Screen

# Search Movies Seat

# Book Movie

# Verify Ticket

# Payment Confirmation

