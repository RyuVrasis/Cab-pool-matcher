class RideRequest:

    def __init__(self, name, city, time, year, request_num):
        self.name = name
        self.city = city
        self.time = time
        self.year = year
        self.request_num = request_num

    def __str__(self):
        return f"{self.request_num},{self.name} year {self.year} going to {self.city} at {self.time} "


class Cab:

    def __init__(self, driver_name, seat_num, destination, dep_time):
        self.driver_name = driver_name
        self.seat_num = seat_num
        self.destination = destination
        self.dep_time = dep_time
        self.has_left = False
        self.student_list = []

    def free_seats(self):
        return self.seat_num - len(self.student_list())

    def __str__(self):
        return f"driver {self.driver_name},cab having seat {len(self.student_list)}/{self.seat_num}  to {self.destination} at {self.dep_time};has left {self.has_left}"
