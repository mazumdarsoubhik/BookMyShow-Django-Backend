from django.db import models


class UserType(models.TextChoices):
    CUSTOMER = "CUSTOMER"
    ORGANIZER = "ORGANIZER"
    MANAGER = "MANAGER"


class Gender(models.TextChoices):
    MALE = "MALE"
    FEMALE = "FEMALE"


class EventType(models.TextChoices):
    CINEMA = "CINEMA"
    ACT = "ACT"
    STADIUM = "STADIUM"


class MovieCategory(models.TextChoices):
    ACTION = "ACTION"
    DRAMA = "DRAMA"
    HORROR = "HORROR"
    COMEDY = "COMEDY"


class MovieScreeningStatus(models.TextChoices):
    UPCOMING = "UPCOMING"
    SHOWING = "SHOWING"
    DISCONTINUED = "DISCONTINUED"


class SeatType(models.TextChoices):
    PLATINUM = "PLATINUM"
    GOLD = "GOLD"
    SILVER = "SILVER"


class SeatStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    LOCKED = "LOCKED"


class ScreenType(models.TextChoices):
    TWO_D = "2D"
    THREE_D = "3D"


class BookingStatus(models.TextChoices):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    EXPIRED = "EXPIRED"


class PaymentMode(models.TextChoices):
    UPI = "UPI"
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    NET = "NET"


class PaymentStatus(models.TextChoices):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    FAILED = "FAILED"

