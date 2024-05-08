from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .enums import *


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(BaseModel):
    name = models.CharField(max_length=255)


class User(BaseModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    userType = models.CharField(choices=UserType.choices, max_length=50)

    class Meta:
        abstract = True


class AppAdmin(User):
    pass


class Customer(User):
    gender = models.CharField(choices=Gender.choices, max_length=50)
    date_of_birth = models.DateField()


class Organizer(User):
    GSTIN = models.CharField(max_length=255)
    Account_number = models.CharField(max_length=255)
    IFSC = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    eventType = models.CharField(choices=EventType.choices, max_length=50)


class Manager(User):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)


class Event(BaseModel):
    eventType = models.CharField(choices=EventType.choices, max_length=50)

    class Meta:
        abstract = True


class Language(BaseModel):
    name = models.CharField(max_length=15)


class MovieCast(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class Movie(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    release_date = models.DateField()
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    movieCategory = models.CharField(choices=MovieCategory.choices, max_length=50)
    casts = models.ManyToManyField(MovieCast, related_name='movies')
    languages = models.ManyToManyField(Language)
    duration = models.IntegerField(null=False, blank=False, default=None)

    def __str__(self):
        return self.title


class MovieTheater(Event):
    name = models.CharField(max_length=30, null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)


class MovieScreen(BaseModel):
    number = models.IntegerField(null=False, blank=False)
    movieTheater = models.ForeignKey(MovieTheater, on_delete=models.CASCADE, related_name='screens', default=None)
    screenType = models.CharField(choices=ScreenType.choices, max_length=50)


class MovieSeat(BaseModel):
    movie_screen = models.ForeignKey(MovieScreen, on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField()
    column = models.IntegerField()
    seatType = models.CharField(choices=SeatType.choices, max_length=50)


class MovieShow(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shows', default=None)
    movieTheater = models.ForeignKey(MovieTheater, on_delete=models.CASCADE, related_name='shows')
    languages = models.ManyToManyField(Language)
    movieScreeningStatus = models.CharField(choices=MovieScreeningStatus.choices, max_length=50, default=None)


class MovieShowScreen(BaseModel):
    movieShow = models.ForeignKey(MovieShow, on_delete=models.CASCADE, related_name='screens')
    movieScreen = models.ForeignKey(MovieScreen, on_delete=models.CASCADE)
    screeningDate = models.DateField()
    screeningStartTime = models.TimeField()


class MovieShowSeat(BaseModel):
    movieShowScreen = models.ForeignKey(MovieShowScreen, on_delete=models.CASCADE, related_name='seats')
    movieSeat = models.ForeignKey(MovieSeat, on_delete=models.CASCADE)
    seatStatus = models.CharField(choices=SeatStatus.choices, max_length=50)
    lockedAt = models.DateTimeField(null=True, blank=True)
    price = models.IntegerField()


class Payment(BaseModel):
    paymentMode = models.CharField(choices=PaymentMode.choices, max_length=50)
    paymentStatus = models.CharField(choices=PaymentStatus.choices, max_length=50)


class Ticket(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    movieTheater = models.ForeignKey(MovieTheater, on_delete=models.CASCADE)
    movieScreen = models.ForeignKey(MovieScreen, on_delete=models.CASCADE)
    selectedSeats = models.ManyToManyField(MovieShowSeat)


class Booking(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    movieShowScreen = models.ForeignKey(MovieShowScreen, on_delete=models.CASCADE, related_name='bookings', default=None)
    selectedSeats = models.ManyToManyField(MovieShowSeat)
    amount = models.FloatField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='booking')
    bookingStatus = models.CharField(choices=BookingStatus.choices, max_length=50)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='booking', default=None)














