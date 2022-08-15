class Reservation:
    def __init__(self, time, table_id):
        self.time = time    # time is an integer YYYYMMDDHH 2022081513 and HH is in 24-hour style; it represent the starting time of the reservation
        self.table_id = table_id    # table_id is a two integer tuple (i, j), which are the indices in restaurant.tables


class Restaurant:
    def __init__(self):
        # 2D list where each index represent table.size-1, and a list of tables nested in
        # [
        # [],                   # index 0, table size 1
        # [table_1, table_2],   # index 1, table size 2
        # [],                   # index 2, table size 3
        # [table_5]             # index 3, table size 4
        # ]
        self.tables = []

    def add_table(self, table):
        while table.size > len(self.tables):
            self.tables.append([])
        self.tables[table.size-1].append(table)

    def reserve_table(self, party_size, req_time):
        # no table available
        if party_size > len(self.tables):
            return None

        for i in range(party_size - 1, len(self.tables)):
            group_tables = self.tables[i]
            if not group_tables:
                continue
            for j in range(len(group_tables)):
                table = group_tables[j]
                reservation_try = table.add_reservation(req_time, (i, j))
                if not reservation_try:
                    continue
                return reservation_try

        # no table available
        return None

    def cancel_reservation(self, reservation):
        i, j = reservation.table_id[0], reservation.table_id[1]
        reserved_table = self.tables[i][j]
        reserved_table.reservations.remove(reservation.time)


class Table:
    def __init__(self, size):
        self.size = size
        self.reservations = []  # a list of starting times of reservations in YYYYMMDDHH style

    def add_reservation(self, req_time, table_id):
        if not self.reservations:
            self.reservations.append(req_time)
            return Reservation(req_time, table_id)

        prev, following = self.__find_prev_next(req_time)
        if req_time > prev + 2 and req_time + 2 < following:
            self.reservations.append(req_time)
            self.reservations.sort()
            return Reservation(req_time, table_id)

        return None

    def __find_prev_next(self, req_time):
        # binary search find the prev and following reservation starting time
        # need to implement
        prev, following = float('inf'), -float('inf')
        return prev, following
