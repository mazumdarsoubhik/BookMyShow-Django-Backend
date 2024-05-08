from rest_framework import serializers
from datetime import datetime, time
from .enums import *


### Custom Serializer Fields ###
class Custom24HRSTimeField(serializers.Field):
    def to_representation(self, value):
        # Convert time object to string in "HHMM" format
        return value.strftime('%H%M')

    def to_internal_value(self, data):
        # Convert string in "HHMM" format to time object
        hour = int(data[:2])
        minute = int(data[2:])
        return time(hour=hour, minute=minute)

###############################


### Data Trasfer Objects ###


class SearchMovieInput(serializers.Serializer):
    city_id = serializers.IntegerField()
    on_date = serializers.DateField()


class SearchMovieOutput(serializers.Serializer):
    movieShow_id = serializers.IntegerField()
    movie_name = serializers.CharField()
    rating = serializers.FloatField()
    duration = serializers.IntegerField()
    movie_casts_name = serializers.ListSerializer(child=serializers.CharField())
    movie_theater_name = serializers.CharField()
    organizer_name = serializers.CharField()
    languages = serializers.ListSerializer(child=serializers.CharField())
    city_name = serializers.CharField()


class CreateMovieShowDTO(serializers.Serializer):
    movie_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    movieTheater_id = serializers.IntegerField()
    language_ids = serializers.ListSerializer(child=serializers.IntegerField())
    movieScreeningStatus = serializers.CharField()
    organizer_id = serializers.IntegerField()


class AddSeatDTO(serializers.Serializer):
    movie_screen_id = serializers.IntegerField()
    seat_list = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField(min_value=0)))
    row_seat_type = serializers.DictField(child=serializers.ListField(child=serializers.IntegerField(min_value=0)))


class MovieShowScreenDTO(serializers.Serializer):
    movie_show_id = serializers.IntegerField()
    movie_screen_id = serializers.IntegerField()
    screening_date = serializers.DateField()
    screening_time_24_hrs = Custom24HRSTimeField()
    base_price = serializers.IntegerField()


class MovieScreeningDTO(serializers.Serializer):
    movie_show_id = serializers.IntegerField()
    on_date = serializers.DateField()


class CreateBookingDTO(serializers.Serializer):
    customer_id = serializers.IntegerField()
    movie_show_screen_id = serializers.IntegerField()
    movie_seat_ids = serializers.ListSerializer(child=serializers.IntegerField())


class PaymentCompletionDTO(serializers.Serializer):
    booking_id = serializers.IntegerField()
    payment_id = serializers.IntegerField()
    amount = serializers.FloatField()
    payment_mode = serializers.ChoiceField(choices=PaymentMode.choices)
    success = serializers.BooleanField()


class VerifyTicketDTO(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    show_screen_id = serializers.IntegerField()

