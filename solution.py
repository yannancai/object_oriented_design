# Add items to the vending machine in fixed number of slots
# Payment using card or cash
# Select item to dispense


from abc import ABC, abstractmethod


class VendingMachine:
    def __init__(self, slot_amount, slot_limit):
        self.slots = [Slot(id, None, slot_limit) for id in range(slot_amount)]
        self.__item_map = {}

    def get_status(self) -> None:
        for slot in self.slots:
            slot.get_status()
        print(self.__item_map)

    def sell(self, slot_id, payment, amount=1):

        slot = self.slots[slot_id]
        if not slot.get_item():
            return "CANNOT PURCHASE EMPTY"

        item_name = slot.get_item().name

        if self.__item_map[item_name] < amount:
            return "CANNOT PURCHASE MORE THAN WHAT WE HAVE"

        total_price = slot.get_item().get_price() * amount
        print("total price is", total_price)
        payment_success, change = payment.is_valid(total_price)

        if not payment_success:
            return change

        if payment_success:
            self.__find_remove(item_name, amount)
            return [item_name, amount, change]

    def __find_remove(self, item_name, amount):
        slots_with_item = []
        for slot_with_item in self.slots:
            if slot_with_item.get_item() is not None and slot_with_item.get_item().name == item_name:
                slots_with_item.append(slot_with_item)

        to_get_amount = amount
        for slot in slots_with_item:
            if to_get_amount:
                if slot.get_amount() >= to_get_amount:
                    self.__item_map[slot.get_item().name] -= to_get_amount
                    slot.remove(to_get_amount)
                    to_get_amount = 0
                else:
                    remove_amount = slot.get_amount()
                    to_get_amount -= remove_amount
                    self.__item_map[slot.get_item().name] -= remove_amount
                    slot.remove(remove_amount)

    def load(self, slot_id, item, add_amount):
        slot = self.slots[slot_id]
        facto_add = slot.add_item(item, add_amount)

        if facto_add:
            if facto_add[0].name not in self.__item_map:
                self.__item_map[facto_add[0].name] = facto_add[1]
            else:
                self.__item_map[facto_add[0].name] += facto_add[1]


class Slot:
    def __init__(self, id, item, limit):
        self.id = id
        self.__item = item
        self.limit = limit
        self.__amount = 0

    def remove(self, remove_amount):
        if self.__amount >= remove_amount:
            self.__amount -= remove_amount
            if self.__amount == 0:
                self.__item = None
        else:
            print("NOT ENOUGH TO REMOVE")

    def add_item(self, item, add_amount):
        if self.__item is not None and item != self.__item:
            print("CANNOT ADD DIFFERENT ITEM")
            return
        if self.__item is None:
            self.__item = item
        if self.__amount + add_amount > self.limit:
            add_amount = self.limit - self.__amount

        self.__amount += add_amount
        return self.__item, add_amount

    def get_item(self):
        return self.__item

    def get_amount(self):
        return self.__amount

    def get_status(self):
        if not self.get_item():
            print([self.id, None])
        else:
            print([self.id, self.__item.name, self.__amount, "$", self.__item.get_price()])


class Item:
    def __init__(self, name, price):
        self.name = name
        self.__price = price

    def set_price(self, price):
        self.__price = price

    def get_price(self):
        return self.__price


class Payment(ABC):
    @abstractmethod
    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def is_valid(self, price):
        pass


class CashPayment(Payment):
    def __init__(self, amount):
        super().__init__(amount)

    def is_valid(self, price):
        if self.amount >= price:
            print("Purchase successful")
            change = self.amount - price
            print("change is", change)
            return True, change
        else:
            print("Purchase failed")
            return False, self.amount


class CreditPayment(Payment):
    def __init__(self, amount=2000):
        super().__init__(amount)

    def is_valid(self, price):
        if self.amount >= price:
            print("Purchase successful")
            return True, "card"
        else:
            print("Purchase failed")
            return False, "card"


my_vending = VendingMachine(5, 3)
my_vending.get_status()

apple = Item("apple", 2)
banana = Item("banana", 1)

my_vending.load(0, apple, 10)
my_vending.load(1, apple, 3)
my_vending.load(2, banana, 10)
my_vending.load(2, apple, 1)
my_vending.load(4, banana, 1)
my_vending.get_status()

cash_10 = CashPayment(10)
purchase_result_1 = my_vending.sell(2, cash_10, 1)
print(purchase_result_1)

my_vending.get_status()
credit_1 = CreditPayment(1)
purchase_result_2 = my_vending.sell(0, credit_1, 2)
print(purchase_result_2)
my_vending.get_status()

purchase_result_3 = my_vending.sell(3, credit_1)
print(purchase_result_3)

credit_2 = CreditPayment()
purchase_result_4 = my_vending.sell(0, credit_2, 4)
my_vending.get_status()

purchase_result_5 = my_vending.sell(1, credit_2, 10)
print(purchase_result_5)
