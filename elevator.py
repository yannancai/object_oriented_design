from abc import ABC, abstractmethod


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
        self.__up_queue = [False] * self.floors
        self.__down_queue = [False] * self.floors
        self.__undirected_queue = [False] * self.floors
        self.__status = Status.IDLE
        self.__current_floor = 1

    def handle_request(self, request):
        request.add_request_to_queue(self.__up_queue, self.__down_queue, self.__undirected_queue)

        if self.__status == Status.IDLE:
            self.__status = request.adjust_status(self.__current_floor)
            
        # print(self.__up_queue, self.__down_queue, self.__undirected_queue)
        # print(self.__status)

    # go to the next in request queue
    # cancel the request from the queue
    def open_door(self):

        if self.__status == Status.UP:
            for i in range(self.__current_floor - 1, self.floors):
                if self.__up_queue[i] or self.__undirected_queue[i]:
                    # move the elevator to the next in request queue
                    self.__current_floor = i + 1

                    # cancel the request from the queue
                    self.__up_queue[i] = False
                    self.__undirected_queue[i] = False

        elif self.__status == Status.DOWN:
            for i in range(self.__current_floor - 1, -1, -1):
                if self.__down_queue[i] or self.__undirected_queue[i]:
                    # move the elevator to the next in request queue
                    self.__current_floor = i + 1

                    # cancel the request from the queue
                    self.__down_queue[i] = False
                    self.__undirected_queue[i] = False

        # print(self.__up_queue, self.__down_queue, self.__undirected_queue)
        # print(self.__status)
                    
        return "door opens on", self.__current_floor

    # change the status and move elevator when needed
    def close_door(self):

        if True not in self.__up_queue and True not in self.__down_queue and \
                True not in self.__undirected_queue:
            self.__status = Status.IDLE
            return "No MORE REQUESTS"

        elif self.__status == Status.UP:
            # there is up or undirected requests in range (current floor, top floor)
            if True in self.__up_queue[self.__current_floor - 1:] or \
                    True in self.__undirected_queue[self.__current_floor - 1:]:
                # self.open_door() will handle it
                return "NO direction/floor adjustments"

            # no more up or undirected requests in range (current floor, top floor)
            # find down request in range (top floor, bottom floor)
            for i in range(self.floors - 1, -1, -1):
                if self.__down_queue[i] or self.__undirected_queue[i]:
                    # change status
                    self.__status = Status.DOWN
                    # move elevator over
                    self.__current_floor = i + 1
                    return "elevator moves to", self.__current_floor

            # find up request in range(bottom floor, top floor)
            for i in range(self.floors):
                if self.__up_queue[i]:
                    # no need to change status
                    # move elevator over
                    self.__current_floor = i + 1
                    return "elevator moves to", self.__current_floor

        elif self.__status == Status.DOWN:
            # there is down or undirected requests in range (bottom floor, current floor)
            if True in self.__down_queue[:self.__current_floor] or \
                    True in self.__undirected_queue[:self.__current_floor]:
                # self.open_door() will handle it
                return "NO direction/floor adjustments"

            # no more down or undirected requests in range (bottom floor, current floor)
            # find up request in range (bottom floor, top floor)
            for i in range(self.floors):
                if self.__up_queue[i] or self.__undirected_queue[i]:
                    # change status
                    self.__status = Status.UP
                    # move elevator over
                    self.__current_floor = i + 1
                    return "elevator moves to", self.__current_floor

            # find down request in range(top floor, bottom floor)
            for i in range(self.floors - 1, -1, -1):
                if self.__up_queue[i]:
                    # no need to change status
                    # move elevator over
                    self.__current_floor = i + 1
                    return "elevator moves to", self.__current_floor


class Request(ABC):
    @abstractmethod
    def __init__(self, floor):
        self.floor = floor

    @abstractmethod
    def add_request_to_queue(self, up_queue, down_queue, undirected_queue):
        pass

    @abstractmethod
    def adjust_status(self, current_floor):
        pass


class OutRequest(Request):
    def __init__(self, floor, direction):
        super().__init__(floor)
        self.direction = direction

    def add_request_to_queue(self, up_queue, down_queue, undirected_queue):
        if self.direction == Direction.UP:
            up_queue[self.floor - 1] = True
        else:
            down_queue[self.floor - 1] = True

    def adjust_status(self, current_floor):
        if current_floor >= self.floor:
            return Status.DOWN
        else:
            return Status.UP


class InRequest(Request):
    def __init__(self, floor):
        super().__init__(floor)

    def add_request_to_queue(self, up_queue, down_queue, undirected_queue):
        undirected_queue[self.floor - 1] = True

    def adjust_status(self, current_floor):
        if current_floor >= self.floor:
            return Status.DOWN
        else:
            return Status.UP


my_elevator = Elevator(5)

request_1 = OutRequest(2, 'DOWN')
request_2 = InRequest(4)

my_elevator.handle_request(request_1)
my_elevator.handle_request(request_2)

msg_open_1 = my_elevator.open_door()
print(msg_open_1)

msg_close_1 = my_elevator.close_door()
print(msg_close_1)

msg_open_2 = my_elevator.open_door()
print(msg_open_2)

msg_close_2 = my_elevator.close_door()
print(msg_close_2)
