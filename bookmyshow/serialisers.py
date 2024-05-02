from rest_framework import serializers
from .models import *
from .dtos import *


class OrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organizer
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CitySerialiser(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class MovieCastSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieCast
        fields = '__all__'


class MovieTheaterSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieTheater
        fields = '__all__'


class MovieScreenSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieScreen
        fields = '__all__'


class MovieSeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieSeat
        fields = '__all__'


class MovieShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieShow
        fields = '__all__'


class MovieShowScreenSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieShowScreen
        fields = '__all__'


class MovieShowSeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieShowSeat
        fields = '__all__'


class AllUserFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserNoPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class BookingSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

