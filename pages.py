'''Pages module for the Coin Tracker Database.'''
from database import (get_data_count, save_coin_to_database, get_coin_types,
                      get_conditions, add_coin_type, add_condition, get_countries, add_country)


def get_page_header(page_name):
    '''Get the page header.'''
    page_name = f"Coin Tracker Database - {page_name}"
    page_name_length = len(page_name)
    page_header_border = "-" * page_name_length

    page_header = f"{page_header_border}\n{page_name}\n{page_header_border}\n"

    return page_header


def main_page():
    '''Main Page function.'''
    while True:
        print(get_page_header("Main Menu"))
        coin_count = get_data_count()

        if coin_count == 1:
            print(f"There is {coin_count} coin in the database.\n")
        else:
            print(f"There are {coin_count} coins in the database.\n")

        print("OPTIONS:")
        if coin_count > 0:
            print("1. View Coins")
            print("2. Insert Data")
            print("3. Update Data")
            print("4. Delete Data")
            print("5. Exit\n")
        else:
            print("1. Insert Data")
            print("2. Exit\n")

        choice = input("Enter your choice: ")

        if coin_count > 0:
            if choice == "1":
                view_coins_page()
            elif choice == "2":
                insert_data_page()
            elif choice == "3":
                update_data_page()
            elif choice == "4":
                delete_data_page()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("** Invalid choice **\n")
        else:
            if choice == "1":
                insert_data_page()
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("** Invalid choice **\n")


def insert_data_page():
    '''Insert Data page.'''
    while True:
        print(get_page_header("Insert Data"))

        print("OPTIONS:")
        print("1. Add New Coin")
        print("2. Add New Coin Type")
        print("3. Add New Condition")
        print("4. Add New Country")
        print("5. Back to Main Menu\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_coin_page()
        elif choice == "2":
            add_coin_type_page()
        elif choice == "3":
            add_condition_page()
        elif choice == "4":
            add_country_page()
        elif choice == "5":
            break  # Go back to main menu
        else:
            print("** Invalid choice **\n")


def view_coins_page():
    '''View Coins page.'''
    print(get_page_header("View Coins"))
    print("View coins functionality coming soon...")
    input("\nPress Enter to continue...")


def update_data_page():
    '''Update Data page.'''
    print(get_page_header("Update Data"))
    print("Update data functionality coming soon...")
    input("\nPress Enter to continue...")


def delete_data_page():
    '''Delete Data page.'''
    print(get_page_header("Delete Data"))
    print("Delete data functionality coming soon...")
    input("\nPress Enter to continue...")


def add_coin_page():
    '''Add New Coin page.'''
    print(get_page_header("Add New Coin"))

    coin_data = get_coin_input()
    save_coin_to_database(coin_data)
    print("Coin added successfully!")


# Add Coin Helper functions
def get_coin_input():
    '''Get coin input from the user.'''
    # Get coin type
    coin_types = get_coin_types()
    print("\nAvailable Coin Types:")
    for i, coin_type in enumerate(coin_types, 1):
        print(f"{i}. {coin_type['name']}")
    print(f"{len(coin_types) + 1}. Add New Coin Type")

    while True:
        try:
            type_choice = int(input("Select coin type: "))
            if 1 <= type_choice <= len(coin_types):
                type_id = coin_types[type_choice - 1]['id']
                break
            elif type_choice == len(coin_types) + 1:
                new_type_name = input("Enter new coin type name: ")
                type_id = add_coin_type(new_type_name)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    # Get condition
    conditions = get_conditions()
    print("\nAvailable Conditions:")
    for i, condition in enumerate(conditions, 1):
        print(f"{i}. {condition['name']}")
    print(f"{len(conditions) + 1}. Add New Condition")

    while True:
        try:
            condition_choice = int(input("Select condition: "))
            if 1 <= condition_choice <= len(conditions):
                condition_id = conditions[condition_choice - 1]['id']
                break
            elif condition_choice == len(conditions) + 1:
                new_condition_name = input("Enter new condition name: ")
                condition_id = add_condition(new_condition_name)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    return {
        "type_id": type_id,
        "year": input("Year: "),
        "mint_mark": input("Mint Mark: "),
        "condition_id": condition_id,
        "quantity": input("Quantity: "),
        "value_estimate": input("Value Estimate: "),
        "acquired_from": input("Acquired From: "),
        "notes": input("Notes: ")}


def add_coin_type_page():
    '''Add New Coin Type page.'''
    print(get_page_header("Add New Coin Type"))
    print("Add coin type functionality coming soon...")
    input("\nPress Enter to continue...")


def add_condition_page():
    '''Add New Condition page.'''
    print(get_page_header("Add New Condition"))
    print("Add condition functionality coming soon...")
    input("\nPress Enter to continue...")


def add_country_page():
    '''Add New Country page.'''
    print(get_page_header("Add New Country"))
    print("Add country functionality coming soon...")
    input("\nPress Enter to continue...")
