from abc import ABC, abstractmethod
from collections import deque


class Node:
    def __init__(self, name, is_directory: bool, extension, size: int):
        self.name = name
        self.is_directory = is_directory
        self.extension = extension
        self.size = size
        self.children = []

    def set_children(self, node):
        self.children.append(node)


class LinuxSearch:
    def search(self, criteria, node):
        if not node.is_directory:
            raise Exception("Node is not directory")

        search_result = []
        queue = deque()

        for child in node.children:
            queue.append(child)

        while queue:
            cur_node = queue.popleft()
            if criteria.is_valid(cur_node):
                search_result.append(cur_node)
            if cur_node.children:
                for child in cur_node.children:
                    queue.append(child)

        return search_result


class Criteria(ABC):
    @abstractmethod
    def is_valid(self, node):
        pass


class ByExtension(Criteria):
    def __init__(self, extension):
        self.extension = extension

    def is_valid(self, node):
        if node.extension is self.extension:
            return True


class ByNodeSize(Criteria, ABC):
    @abstractmethod
    def __init__(self, size):
        self.size = size

    @abstractmethod
    def is_valid(self, node):
        pass


class ByGreatOrEqual(ByNodeSize):
    def __init__(self, size):
        super().__init__(size)

    def is_valid(self, node):
        if node.size >= self.size:
            return True


class AndCriteria(Criteria):
    def __init__(self, criteria_a, criteria_b):
        self.criteria_a = criteria_a
        self.criteria_b = criteria_b

    def is_valid(self, node):
        return self.criteria_a.is_valid(node) and self.criteria_b.is_valid(node)


class OrCriteria(Criteria):
    def __init__(self, criteria_a, criteria_b):
        self.criteria_a = criteria_a
        self.criteria_b = criteria_b

    def is_valid(self, node):
        return self.criteria_a.is_valid(node) or self.criteria_b.is_valid(node)


home = Node("home", True, None, 100)
movie = Node("movie", True, None, 70)
music = Node("music", True, None, 20)
resume = Node("resume", False, "txt", 10)
alpha = Node("alpha", False, "txt", 15)
beta = Node("beta", False, "mp4", 60)
gamma = Node("gamma", False, "mp4", 15)
cuban = Node("cuban", True, None, 5)

home.set_children(movie)
home.set_children(music)
home.set_children(resume)
movie.set_children(alpha)
movie.set_children(beta)
music.set_children(gamma)
music.set_children(cuban)

my_linux = LinuxSearch()

is_txt = ByExtension("txt")
search_home_txt = my_linux.search(is_txt, home)
print("search_home_txt")
print([(node.name, node.size) for node in search_home_txt])

is_size_ge_15 = ByGreatOrEqual(15)
search_movie_ge_15 = my_linux.search(is_size_ge_15, movie)
print("search_movie_ge_15")
print([(node.name, node.size) for node in search_movie_ge_15])

is_txt_ge_15 = AndCriteria(is_txt, is_size_ge_15)
search_home_txt_ge_15 = my_linux.search(is_txt_ge_15, home)
print("search_home_txt_ge_15")
print([(node.name, node.size) for node in search_home_txt_ge_15])

is_mp4 = ByExtension("mp4")
search_home_mp4 = my_linux.search(is_mp4, home)
print("search_home_mp4")
print([(node.name, node.size) for node in search_home_mp4])

# txt ge 15 or mp4
is_home_comp = OrCriteria(is_txt_ge_15, is_mp4)
search_home_comp = my_linux.search(is_home_comp, home)
print("search_home_comp")
print([(node.name, node.size) for node in search_home_comp])

search_gamma = my_linux.search(is_txt, gamma)
