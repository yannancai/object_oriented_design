from abc import ABC, abstractmethod
import heapq


class Status:
    UP = 'UP'
    DOWN = 'DOWN'
    IDLE = 'IDLE'


class Direction:
    UP = 'UP'
    DOWN = 'DOWN'


class Elevator:
    def __init__(self, floors):
        self.floors = floors
        self.__up_first_min = []
        self.__up_second_min = []
        self.__down_first_max = []
        self.__down_second_max = []
        self.__status = Status.IDLE
        self.__current_floor = 1

    def add_request(self, request):
        request_direction = request.get_direction(self.__status, self.__current_floor)

        if self.__status == Status.IDLE:
            self.__status = request_direction

        if self.__status == Status.UP:
            if request_direction == Direction.UP and request.floor >= self.__current_floor:
                heapq.heappush(self.__up_first_min, request.floor)
            elif request_direction == Direction.UP and request.floor < self.__current_floor:
                heapq.heappush(self.__up_second_min, request.floor)
            else:
                heapq.heappush(self.__down_first_max, request.floor)

        else:
            if request_direction == Direction.DOWN and request.floor <= self.__current_floor:
                heapq.heappush(self.__down_first_max, request.floor)
            elif request_direction == Direction.UP and request.floor > self.__current_floor:
                heapq.heappush(self.__down_second_max, request.floor)
            else:
                heapq.heappush(self.__up_first_min, request.floor)

    def find_and_complete_next_request(self):

        self.__adjust_direction()

        if self.__status == Status.IDLE:
            return None

        if self.__status == Status.UP:
            next_floor = heapq.heappop(self.__up_first_min)
        else:
            next_floor = heapq.heappop(self.__down_first_max)

        self.__current_floor = next_floor
        return next_floor, self.__status, self.__up_first_min, self.__up_second_min, self.__down_first_max, self.__down_second_max

    def __adjust_direction(self):
        if self.__status == Status.UP:
            if self.__up_first_min:
                return
            elif self.__down_first_max:
                self.__status = Status.DOWN
                self.__up_first_min, self.__up_second_min = self.__up_second_min, self.__up_first_min
                return
            elif self.__up_second_min:
                self.__up_first_min, self.__up_second_min = self.__up_second_min, self.__up_first_min
                return
            else:
                self.__status = Status.IDLE

        elif self.__status == Status.DOWN:
            if self.__down_first_max:
                return
            elif self.__up_first_min:
                self.__status = Status.UP
                self.__down_first_max, self.__down_second_max = self.__down_second_max, self.__down_first_max
                return
            elif self.__down_second_max:
                self.__down_first_max, self.__down_second_max = self.__down_second_max, self.__down_first_max
                return
            else:
                self.__status = Status.IDLE


class Request(ABC):
    @abstractmethod
    def __init__(self, floor):
        self.floor = floor

    @abstractmethod
    def get_direction(self, elevator_status, elevator_floor):
        pass


class OutRequest(Request):
    def __init__(self, floor, direction):
        super().__init__(floor)
        self.direction = direction

    def get_direction(self, elevator_status, elevator_floor):
        return self.direction


class InRequest(Request):
    def __init__(self, floor):
        super().__init__(floor)
        self.direction = Direction.UP

    def get_direction(self, elevator_status, elevator_floor):
        if self.floor >= elevator_floor:
            if elevator_status == Status.UP or elevator_status == Status.IDLE:
                self.direction = Direction.UP
            elif elevator_status == Status.DOWN:
                self.direction = Direction.DOWN
        elif self.floor < elevator_floor:
            if elevator_status == Status.DOWN or elevator_status == Status.IDLE:
                self.direction = Direction.DOWN
            elif elevator_status == Status.UP:
                self.direction = Direction.UP

        return self.direction


my_elevator = Elevator(5)

request_1 = OutRequest(2, 'DOWN')
request_2 = InRequest(4)

my_elevator.add_request(request_1)
my_elevator.add_request(request_2)

msg_1 = my_elevator.find_and_complete_next_request()
print(msg_1)

request_3 = OutRequest(3, 'UP')
my_elevator.add_request(request_3)

msg_2 = my_elevator.find_and_complete_next_request()
print(msg_2)

request_4 = InRequest(1)
my_elevator.add_request(request_4)

msg_3 = my_elevator.find_and_complete_next_request()
print(msg_3)

msg_4 = my_elevator.find_and_complete_next_request()
print(msg_4)
