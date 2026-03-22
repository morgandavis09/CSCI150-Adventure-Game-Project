#gamefunctions.py
#Morgan Davis
#2/22/26

#This program is a project and utilizes the functions purchase_item() and new_random_monster().
#The functions are called each three times to demonstrate different scenarios.
#There are added docstrings to the beginning of each of the functions 

"""This module contains different functions that are called to test multiple times.

It uses the import random function.
It consists of purchase_item, new_random_monster, print_welcome, and print_shop_menu.
    Typical usage examples:

    purchase_item(123, 1000, 3)
    print_welcome("Mike", 20)""" 

import random

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """Shows how many items can be bought.
         Parameters:
        itemPrice (int): Cost of one item.
        startingMoney (int): Money available.
        quantityToPurchase (int): Number of items wanted (default is 1).

    Returns:
        Number purchased and leftover money."""

    can_afford = startingMoney // itemPrice
    num_purchased = min(quantityToPurchase, can_afford)
    leftover_money = startingMoney - (num_purchased * itemPrice)
    return num_purchased, leftover_money



def new_random_monster():
    """Creates a randomly generated monster.

    Returns a dictionary containing name, description,
              health, power, and money."""
    monster = random.randint(1, 3)

    if monster == 1:
        name = "Werewolf"
        description = "This is a lone wolf. When it notices you, it charges you with snarling teeth."
        health = random.randint(20, 40)
        power = random.randint(5, 10)
        money = random.randint(10, 50)

    elif monster == 2:
        name = "Vampire"
        description = "You find a vampire sleeping in a cave. You must carefully pass it to get to the other side of the mountain."
        health = random.randint(0, 20)
        power = random.randint(10, 20)
        money = random.randint(100, 10000)

    elif monster == 3:
        name = "Dragon"
        description = "A dragon stands in your way and breaths fire at you."
        health = random.randint(50, 80)
        power = random.randint(70, 100)
        money = random.randint(75, 100)

    my_monster = {}
    my_monster["name"] = name
    my_monster["description"] = description
    my_monster["health"] = health
    my_monster["power"] = power
    my_monster["money"] = money

    return my_monster

def print_welcome(name, width):
    """Prints a welcome message centered in the specified width.
    Parameters:
        name (str): Name 
        width (int): Total width 

    Returns none"""
    message = "Hello, " + name + "!"
    print(f"{message:^{width}}")


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """Prints a small shop menu with two items and their prices.
    Parameters:
        item1Name (str): First item.
        item1Price (float): First item price.
        item2Name (str): Second item.
        item2Price (float): Second item price.

    Returns none"""
    print("/----------------------\\")
    
    price1 = f"${item1Price:.2f}"
    price2 = f"${item2Price:.2f}"
    
    print(f"| {item1Name:<12}{price1:>8} |")
    print(f"| {item2Name:<12}{price2:>8} |")
    
    print("\\----------------------/")


#Calling the functions.
print(purchase_item(123, 1000, 3))   
print(purchase_item(123, 201, 3))    
print(purchase_item(341, 2112))      


monster1 = new_random_monster()
print(monster1)

monster2 = new_random_monster()
print(monster2)

monster3 = new_random_monster()
print(monster3)

print(purchase_item(2.5, 10.75, 3))
print(purchase_item(4.2, 18.9, 2))
print(purchase_item(1.75, 6.5))

print_welcome("Morgan", 20)
print_welcome("Madison", 20)
print_welcome("Mike", 20)

print_shop_menu("Water", 1.25, "Apples", 2.75)
print_shop_menu("Milk", 3.49, "Eggs", 4.89)
print_shop_menu("Flour", 5.55, "Yogurt", 6.35)





