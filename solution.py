class LockerBox:
    def __init__(self, size_list):
        self.__size_list = size_list.sort()
        self.__is_empty = [True] * len(self.__size_list)
        self.__open_id = 0
        self.__dict_openid_index = {}

    def find_empty(self, item_size):
        if item_size > self.__size_list[-1]:
            return None

        start_index = self.__binary_search(item_size)
        for index in range(start_index, len(self.__size_list)):
            if not self.__is_empty[index]:
                continue
            self.__open_id += 1
            self.__dict_openid_index[self.__open_id] = index
            self.__is_empty[index] = False
            return index, self.__open_id    # __open_id is used as item id

        return None

    def find_item(self, open_id):
        if open_id not in self.__dict_openid_index:
            return None
        box_index = self.__dict_openid_index[open_id]
        self.__dict_openid_index.pop(open_id)
        self.__is_empty[box_index] = True
        return box_index

    def __binary_search(self, item_size):
        # a binary search to find the smallest box size which is equal to or larger than item_size
        index = 0
        return index
