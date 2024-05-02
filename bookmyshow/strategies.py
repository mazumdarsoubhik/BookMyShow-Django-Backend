class MovieSeatPriceStrategy:
    @staticmethod
    def get_price(movie_seat_obj: dict, base_price: int) -> int:
        pricingObj = MovieSeatPriceStrategy()
        return pricingObj._version_one(movie_seat_obj, base_price)

    def _version_one(self, movie_seat_obj: dict, base_price: int) -> int:
        if movie_seat_obj["seatType"] == "SILVER":
            return base_price
        if movie_seat_obj["seatType"] == "GOLD":
            return int(base_price * 1.1)
        elif movie_seat_obj["seatType"] == "PLATINUM":
            return int(base_price * 1.2)
        else:
            return base_price
