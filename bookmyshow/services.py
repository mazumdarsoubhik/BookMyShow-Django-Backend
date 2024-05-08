from rest_framework.generics import get_object_or_404
from .models import *
from .serialisers import *
from .strategies import *
from datetime import datetime, timezone
import pdb


class ShowSeatAdditionService:
    @staticmethod
    def execute(movie_show_screen_obj: dict, movie_seats_obj: dict, base_price: int):
        service_obj = ShowSeatAdditionService()
        return service_obj._version_one(movie_show_screen_obj, movie_seats_obj, base_price)

    def _version_one(self, movie_show_screen_obj: dict, movie_seats_obj: dict, base_price: int):
        try:
            if "id" not in movie_show_screen_obj:
                movie_show_screen = MovieShowScreen.objects.get(
                    movieShow=movie_show_screen_obj["movieShow"],
                    movieScreen=movie_show_screen_obj["movieScreen"],
                    screeningDate=movie_show_screen_obj["screeningDate"],
                    screeningStartTime=movie_show_screen_obj["screeningStartTime"]
                )
                serialized_movie_show_screen = MovieShowScreenSerializer(movie_show_screen)
                movie_show_screen_id = serialized_movie_show_screen.data["id"]
            else:
                movie_show_screen_id = movie_show_screen_obj["id"]

            for movieseat in movie_seats_obj:
                show_seat_data = {
                    "movieShowScreen": movie_show_screen_id,
                    "movieSeat": movieseat["id"],
                    "seatStatus": "AVAILABLE",
                    "price": MovieSeatPriceStrategy.get_price(movieseat, base_price)
                }

                serializedShowSeat = MovieShowSeatSerializer(data=show_seat_data)
                if not serializedShowSeat.is_valid():
                    print(f"Error at ShowSeatAdditionService:\n{serializedShowSeat.errors}")
                    return False

                serializedShowSeat.save()
            return True
        except Exception as e:
            print(f"Error at ShowSeatAdditionService: \n{e}")
            return False


class BookingService:
    @staticmethod
    def execute(booking_obj):
        booking_service = BookingService()
        return booking_service._version_one(booking_obj)

    def _version_one(self, booking_obj):

        ### Create Payment ###
        payment_details = {
            "paymentMode": "",
            "paymentStatus": "PENDING"
        }
        payment = PaymentSerializer(data=payment_details)
        if payment.is_valid():
            payment.save()
        else:
            return False, payment.errors

        ### BLOCK the Seats ###
        seats = MovieShowSeat.objects.filter(pk__in=booking_obj["movie_seat_ids"])
        for seat in seats:
            if seat.seatStatus == "AVAILABLE":
                seat.seatStatus = "LOCKED"
                seat.lockedAt = datetime.now(timezone.utc)
                seat.save()
            elif seat.seatStatus == "LOCKED":
                if (datetime.now(timezone.utc) - seat.lockedAt).seconds // 60 > 1:      ## Hold a seat for 1 min
                    seat.lockedAt = datetime.now(timezone.utc)
                    seat.save()
                else:
                    return False, {"message": "Seat is locked by other user."}
            else:
                return False, {"message": "Seat is unavailable."}

        ### Create Ticket ###
        movie_show_screen = get_object_or_404(MovieShowScreen, pk=booking_obj["movie_show_screen_id"])
        ticket_details = {
            "customer": booking_obj["customer_id"],
            "movieTheater": movie_show_screen.movieShow.movieTheater.id,
            "movieScreen": movie_show_screen.movieScreen.id,
            "selectedSeats": booking_obj["movie_seat_ids"]
        }
        ticket = TicketSerializer(data=ticket_details)
        if ticket.is_valid():
            ticket.save()
        else:
            return False, ticket.errors
        # pdb.set_trace()
        booking_data = {
            "customer": booking_obj["customer_id"],
            "movieShowScreen": booking_obj["movie_show_screen_id"],
            "selectedSeats": booking_obj["movie_seat_ids"],
            "amount": sum([get_object_or_404(MovieShowSeat, pk=seat_id).price for seat_id in booking_obj["movie_seat_ids"]]),
            "payment": payment.data["id"],
            "bookingStatus": "PENDING",
            "ticket": ticket.data["id"]
        }
        booking = BookingSerialiser(data=booking_data)
        if booking.is_valid():
            booking.save()
        else:
            return False, booking.errors

        return True, booking.data


class PaymentCompletionService:
    @staticmethod
    def execute(payment_details):
        payment_completion_service = PaymentCompletionService()
        return payment_completion_service._version_one(payment_details)

    def _version_one(self, payment_details):
        booking = get_object_or_404(Booking, pk=payment_details["booking_id"])
        payment = get_object_or_404(Payment, pk=payment_details["payment_id"])
        if payment_details["success"]:
            payment.paymentMode = payment_details["payment_mode"]
            payment.paymentStatus = "SUCCESS"
            booking.bookingStatus = "COMPLETED"
            payment.save()
            booking.save()
            ticket = booking.ticket
            s_ticket = TicketSerializer(ticket)
            return True, s_ticket.data
        else:
            return False, {"message": "Payment Failed."}

