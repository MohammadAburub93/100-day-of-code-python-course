from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
again = True
my_coffe_machine = CoffeeMaker()
money_machine = MoneyMachine()
while again:
    my_menu = Menu()
    user_choice = input(f"What would you like? {my_menu.get_items()}: ")

    if user_choice == "off":
        again = False
    elif user_choice == "report":
        my_coffe_machine.report()
        money_machine.report()
    else:
        user_drink = my_menu.find_drink(user_choice)
        if user_drink:
            if my_coffe_machine.is_resource_sufficient(user_drink):
                if money_machine.make_payment(user_drink.cost):
                    my_coffe_machine.make_coffee(user_drink)
