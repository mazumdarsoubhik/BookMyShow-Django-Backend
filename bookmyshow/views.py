from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .serialisers import *
from .dtos import *
from .strategies import *
from .services import *
import pdb

class Signup(APIView):
    # No Access
    pass


class Login(APIView):
    # ALL user
    pass


class AddCustomer(APIView):
    def post(self, request: Request):
        SerializedCustomer = CustomerSerializer(data=request.data)
        if SerializedCustomer.is_valid():
            SerializedCustomer.save()
            return Response(SerializedCustomer.data, 201)
        else:
            return Response(SerializedCustomer.errors, 400)


class AddOrganizer(APIView):
    def post(self, request: Request):
        SerializedOrganizer = OrganizerSerializer(data=request.data)
        if SerializedOrganizer.is_valid():
            SerializedOrganizer.save()
            return Response(SerializedOrganizer.data, 201)
        else:
            return Response(SerializedOrganizer.errors, 400)


class GetAddCity(APIView):
    def get(self, request: Request):
        # User access
        cities = City.objects.all()
        serializedCities = CitySerialiser(cities, many=True)
        return Response(serializedCities.data, 200)

    def post(self, request: Request):
        # Admin access
        city_exists = City.objects.filter(name=request.data["name"]).exists()
        if city_exists:
            return Response({
                "message": "City Already exists."
            }, 204)

        serializedCity = CitySerialiser(data=request.data)
        if serializedCity.is_valid():
            serializedCity.save()
            return Response(serializedCity.data, 201)
        else:
            return Response(serializedCity.errors, 400)


class DeleteCity(APIView):
    # Admin only
    def delete(self, request: Request, pk: int):
        try:
            city = City.objects.get(pk=pk)
            city.delete()
            serializedCity = CitySerialiser(city)
            return Response(serializedCity.data, 204)
        except NotFound:
            raise NotFound(detail="City not found")
        except Exception as e:
            print(f'Server error:{e}')
            return Response({
                "message": "Some issue faced in delete function",
                "error": e
            },
                500)


class GetAddLanguages(APIView):
    # Admin access
    def get(self, request: Request):
        languages = Language.objects.all()
        serializedLanguages = LanguageSerializer(languages, many=True)
        return Response(serializedLanguages.data, 200)

    def post(self, request: Request):
        language_exists = Language.objects.filter(name=request.data["name"]).exists()
        if language_exists:
            return Response({
                "message": "Language Already exists."
            }, 204)
        serializedLanguage = LanguageSerializer(data=request.data)
        if serializedLanguage.is_valid():
            serializedLanguage.save()
            return Response(serializedLanguage.data, 201)
        else:
            return Response(serializedLanguage.errors, 400)


class GetAddUpdateMovies(APIView):

    def get(self, request):
        movies = Movie.objects.all()
        serializedmovie = MovieSerializer(movies, many=True)
        return Response(serializedmovie.data, 200)

    def post(self, request):
        movie_exists = Movie.objects.filter(title=request.data["title"],
                                            release_date=request.data["release_date"]).exists()
        if movie_exists:
            return Response({
                "message": "Movie already exists"
            }, 204)

        serialized_movie = MovieSerializer(data=request.data)
        if serialized_movie.is_valid():
            serialized_movie.save()
            return Response(serialized_movie.data, 201)
        else:
            return Response(serialized_movie.errors, 400)

    def put(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serialized_movie = MovieSerializer(movie, data=request.data)
            if serialized_movie.is_valid():
                serialized_movie.save()
                return Response(serialized_movie.data, 200)
            else:
                return Response(serialized_movie.errors, 400)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, 404)


class GetAddDeleteUpdateCasts(APIView):
    def get(self, request: Request):
        # Admin
        casts = MovieCast.objects.all()
        serializedCasts = MovieCastSerializer(casts, many=True)
        return Response(serializedCasts.data, 200)

    def post(self, request: Response):
        # Admin
        cast_exists = MovieCast.objects.filter(name=request.data["name"]).exists()
        if cast_exists:
            return Response({
                "message": "Movie cast already exists"
            }, 201)

        SerializedCast = MovieCastSerializer(data=request.data)
        if SerializedCast.is_valid():
            SerializedCast.save()
            return Response(SerializedCast.data, 201)
        else:
            return Response(SerializedCast.errors, 400)

    def put(self, request: Response):
        # Admin
        return Response({"message": "Feature not implemented yet."}, 400)

    def delete(self, request: Response):
        # Admin
        return Response({"message": "Feature not implemented yet."}, 400)


class GetAddMovieTheater(APIView):
    def get(self, request: Response):
        movietheaters = MovieTheater.objects.all()
        serializedMovieTheater = MovieTheaterSerializer(movietheaters, many=True)
        return Response(serializedMovieTheater.data, 200)

    def post(self, request: Request):
        SerializedMovieTheater = MovieTheaterSerializer(data=request.data)
        if SerializedMovieTheater.is_valid():
            SerializedMovieTheater.save()
            return Response(SerializedMovieTheater.data, 201)
        else:
            return Response(SerializedMovieTheater.errors, 400)


class AddGetMovieScreen(APIView):
    def post(self, request: Response):
        serializedMovieScreen = MovieScreenSerializer(data=request.data)
        if serializedMovieScreen.is_valid():
            serializedMovieScreen.save()
            return Response(serializedMovieScreen.data, 201)
        else:
            return Response(serializedMovieScreen.errors, 400)

    def get(self, request: Response):
        movieScreens = MovieScreen.objects.all()
        serializedMovieScreens = MovieScreenSerializer(movieScreens, many=True)
        return Response(serializedMovieScreens.data, 200)


class AddGetMovieSeat(APIView):
    def post(self, request: Response):
        serializedSeats = AddSeatDTO(data=request.data)
        if serializedSeats.is_valid():
            for seat_tuple in serializedSeats.validated_data["seat_list"]:
                temp_seatType = None
                for category in serializedSeats.validated_data["row_seat_type"].keys():
                    row_range = serializedSeats.validated_data["row_seat_type"][category]
                    if row_range[0] <= seat_tuple[0] <= row_range[1]:
                        temp_seatType = category
                        break
                if not temp_seatType:
                    return Response({"seat_list": [f"{seat_tuple[0]} row do not have seat Type mentioned."]}, 400)

                seat_data = {
                    "row": seat_tuple[0],
                    "column": seat_tuple[1],
                    "movie_screen": serializedSeats.validated_data["movie_screen_id"],
                    "seatType": temp_seatType
                }

                movieSeat = MovieSeatSerializer(data=seat_data)
                if not movieSeat.is_valid():
                    return Response(movieSeat.errors, 500)
                movieSeat.save()
            return Response({"message": "All seats are added"}, 201)
        else:
            return Response(serializedSeats.errors, 400)


class AddMovieShow(APIView):
    def post(self, request: Request):
        # Admin
        movieShow_input = CreateMovieShowDTO(data=request.data)
        if not movieShow_input.is_valid():
            return Response(movieShow_input.errors, 400)

        model_data = {
                "name": get_object_or_404(Movie, pk=movieShow_input.validated_data["movie_id"]).title,
                "organizer": movieShow_input.validated_data["organizer_id"],
                "eventType": "CINEMA",
                "movie": movieShow_input.validated_data["movie_id"],
                "city": movieShow_input.validated_data["city_id"],
                "movieTheater": movieShow_input.validated_data["movieTheater_id"],
                "languages": movieShow_input.validated_data["language_ids"],
                "movieScreeningStatus": movieShow_input.validated_data["movieScreeningStatus"]
            }

        serializedMovieShow = MovieShowSerializer(data=model_data)
        if serializedMovieShow.is_valid():
            if MovieShow.objects.filter(movie=serializedMovieShow.validated_data["movie"],
                                        movieTheater=serializedMovieShow.validated_data["movieTheater"]):
                return Response({"message": "Movie in the Theater already exists."}, 204)
            serializedMovieShow.save()
            return Response(serializedMovieShow.data, 201)
        else:
            return Response(serializedMovieShow.errors, 400)

    def get(self, request: Response):
        # Admin
        movieShow = MovieShow.objects.all()
        serializedMovieShow = MovieShowSerializer(movieShow, many=True)
        return Response(serializedMovieShow.data, 200)


class AddMovieShowScreen(APIView):
    def post(self, request: Response):
        inputData = MovieShowScreenDTO(data=request.data)
        if inputData.is_valid():

            show_screen_data = {
                "movieShow": inputData.validated_data["movie_show_id"],
                "movieScreen": inputData.validated_data["movie_screen_id"],
                "screeningDate": inputData.validated_data["screening_date"],
                "screeningStartTime": inputData.validated_data["screening_time_24_hrs"]
            }

            serializedMovieShowScreen = MovieShowScreenSerializer(data=show_screen_data)

            if not serializedMovieShowScreen.is_valid():
                return Response(serializedMovieShowScreen.errors, 500)

            if not MovieShowScreen.objects.filter(
                    movieShow=inputData.validated_data["movie_show_id"],
                    movieScreen=inputData.validated_data["movie_screen_id"],
                    screeningDate=inputData.validated_data["screening_date"],
                    screeningStartTime=inputData.validated_data["screening_time_24_hrs"]).exists:
                serializedMovieShowScreen.save()

            try:
                movieSeats = MovieSeat.objects.filter(movie_screen_id=inputData.validated_data["movie_screen_id"])
                serializedMovieSeats = MovieSeatSerializer(movieSeats, many=True)

                for retry in range(5):
                    try:
                        if ShowSeatAdditionService.execute(serializedMovieShowScreen.data,
                                                           serializedMovieSeats.data,
                                                           inputData.validated_data["base_price"]):
                            return Response({
                                "seat_service_execution": True,
                                "message": "Movie Show's Screen is added. Seats are initiated successfully."},
                                201)
                    except Exception as e:
                        print(f'ERROR: \nIn try block of the function \n{e} \n\nRetry seat adding service')

            except Exception as e:
                print(f'ERROR: \nIn try block of the function \n{e}')

            return Response({
                "seat_service_execution": False,
                "message": "Show Screen is added but failed to run Seat service.",
                "data": serializedMovieShowScreen.data},
                500)
        else:
            return Response(inputData.errors, 400)


class SearchMoviesByCity(APIView):
    def get(self, request):
        # Users
        inputData = SearchMovieInput(data=request.query_params)
        if inputData.is_valid():
            city = get_object_or_404(City, pk=inputData.validated_data["city_id"])
            movieShows = city.shows.all()
            outputResponse=[]
            for movieShow in movieShows:
                movieShow_data = {
                    'movieShow_id': movieShow.id,
                    'movie_name': movieShow.movie.title,
                    'rating': movieShow.movie.rating,
                    'duration': movieShow.movie.duration,
                    'movie_casts_name': [cast.name for cast in movieShow.movie.casts.all()],
                    'movie_theater_name': movieShow.movieTheater.name,
                    'organizer_name': movieShow.movieTheater.organizer.firstname,
                    'languages': [language.name for language in movieShow.movie.languages.all()],
                    'city_name': movieShow.city.name
                }
                serializedOutput = SearchMovieOutput(data=movieShow_data)
                if not serializedOutput.is_valid():
                    return Response({serializedOutput.errors}, 500)
                outputResponse.append(serializedOutput.data)

            return Response(outputResponse, 200)
        else:
            return Response(inputData.errors, 400)


class MovieScreeningDetails(APIView):
    def get(self, request: Request):
        querydetails = MovieScreeningDTO(data=request.query_params)
        if querydetails.is_valid():
            movieShow = get_object_or_404(MovieShow, pk=querydetails.validated_data["movie_show_id"])
            movieShowScreens = movieShow.screens.all()

            output_response=[]

            for movie_show_screen in movieShowScreens:
                movie_screening_details = {
                    "movie_show_screen_id": movie_show_screen.id,
                    "movie_show_id": movieShow.id,
                    "movie_name": movieShow.movie.title,
                    "movie_date": movie_show_screen.screeningDate,
                    "movie_start_time": movie_show_screen.screeningStartTime,
                    "movie_theater_name": movieShow.movieTheater.name,
                    "organizer_name": movieShow.movieTheater.organizer.firstname,
                    "screen_type": movie_show_screen.movieScreen.screenType,
                    "seat_type": movieShow.movie.title
                }

                output_response.append(movie_screening_details)

            return Response(output_response, 200)
        else:
            return Response(querydetails.errors, 400)


class GetMovieShowSeats(APIView):
    def get(self, request):
        if "movie_show_screen_id" in request.query_params and type(request.query_params["movie_show_screen_id"]):
            movie_show_screen = MovieShowScreen.objects.get(pk=request.query_params["movie_show_screen_id"])
            seats = movie_show_screen.seats.all()
            s_seats = MovieShowSeatSerializer(seats, many=True)
            return Response(s_seats.data, 200)
        else:
            return Response({"message": "Invalid query parameter.",
                             "format": ["?movie_show_screen_id=(int)"]}, 400)


class CreateBooking(APIView):
    # User
    def post(self, request: Request):
        booking_details = CreateBookingDTO(data=request.data)
        if booking_details.is_valid():
            service_status, response_data = BookingService.execute(booking_details.data)
            if service_status:
                return Response(response_data, 200)
            else:
                return Response(response_data, 500)
        else:
            return Response(booking_details.errors, 400)


class MakePayment(APIView):
    def post(self, request: Request):
        payment_details = PaymentCompletionDTO(data=request.data)
        if payment_details.is_valid():
            service_status, response_data = PaymentCompletionService.execute(payment_details.data)
            if service_status:
                return Response(response_data, 200)
            else:
                return Response(response_data, 400)
        else:
            return Response(payment_details.errors, 400)


class VerifyTicket(APIView):
    def get(self, request: Request):
        # Manager
        reconcile_details = VerifyTicketDTO(data=request.data)
        if reconcile_details.is_valid():
            ticket = get_object_or_404(Ticket, pk=reconcile_details.validated_data["ticket_id"])
            screen = get_object_or_404(MovieShowScreen, pk=reconcile_details.validated_data["show_screen_id"])
            booking = get_object_or_404(Booking, ticket=ticket.id)
            ## Check if show belongs to manager ##

            ## Check if ticket belongs to show screen ##
            # pdb.set_trace()
            if booking.movieShowScreen.id == screen.id:
                s_ticket = TicketSerializer(ticket)
                return Response({"valid": True,
                                 "message": "Ticket Verified",
                                 "data": s_ticket.data},
                                200)
            else:
                return Response({"valid": False,
                                 "message": "Invalid ticket."},
                                200)
        else:
            return Response({"valid": False,
                             "data": reconcile_details.errors},
                            400)


