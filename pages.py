"""Pages module for the Coin Tracker Database."""

from models.coin import Coin
from models.coin_type import CoinType
from database import (
    get_data_count,
    get_coins_with_details,
    save_coin_to_database,
    get_coin_types,
    save_coin_type_to_database,
    get_conditions,
    add_coin_type,
    add_condition,
)


def get_page_header(page_name: str) -> str:
    """Get the page header."""
    page_name = f"Coin Tracker Database - {page_name}"
    page_name_length = len(page_name)
    page_header_border = "-" * page_name_length

    page_header = f"{page_header_border}\n{page_name}\n{page_header_border}\n"

    return page_header


def main_page():
    """Main Page function."""
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
    """Insert Data page."""
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
    """View Coins page."""
    print(get_page_header("View Coins"))

    coins = get_coins_with_details()

    if not coins:
        print("No coins found in the database.")
        input("\nPress Enter to continue...")
        return

    # Display coins in a formatted table
    print(
        f"{'ID':<4} {'Coin Type':<20} {'Year':<6} {'Mint':<6} {'Condition':<12} {'Qty':<4} "
        f"{'Value':<8} {'Country':<12} {'Acquired From':<15}"
    )
    print("-" * 120)

    for coin in coins:
        # Format the data for display
        coin_id = str(coin["id"])
        coin_type = coin["coin_type_name"] or "Unknown"
        year = str(coin["year"]) if coin["year"] else "N/A"
        mint_mark = coin["mint_mark"] or "N/A"
        condition = coin["condition_name"] or "Unknown"
        quantity = str(coin["quantity"]) if coin["quantity"] else "N/A"
        value = (
            f"${float(coin['value_estimate']):.2f}" if coin["value_estimate"] else "N/A"
        )
        country = coin["country_name"] or "Unknown"
        acquired_from = coin["acquired_from"] or "N/A"

        # Truncate long strings for better display
        coin_type = coin_type[:18] + ".." if len(coin_type) > 20 else coin_type
        condition = condition[:10] + ".." if len(condition) > 12 else condition
        country = country[:10] + ".." if len(country) > 12 else country
        acquired_from = (
            acquired_from[:13] + ".." if len(acquired_from) > 15 else acquired_from
        )

        print(
            f"{coin_id:<4} {coin_type:<20} {year:<6} {mint_mark:<6} {condition:<12} "
            f"{quantity:<4} {value:<8} {country:<12} {acquired_from:<15}"
        )

    input("\nPress Enter to continue...")


def update_data_page():
    """Update Data page."""
    print(get_page_header("Update Data"))
    print("Update data functionality coming soon...")
    input("\nPress Enter to continue...")


def delete_data_page():
    """Delete Data page."""
    print(get_page_header("Delete Data"))
    print("Delete data functionality coming soon...")
    input("\nPress Enter to continue...")


def add_coin_page():
    """Add New Coin page."""
    print(get_page_header("Add New Coin"))

    coin_data = get_coin_input()
    save_coin_to_database(coin_data)
    print("Coin added successfully!")


def get_coin_input():
    """Get coin input from the user."""
    coin = Coin()

    coin_types = get_coin_types()
    print("\nAvailable Coin Types:")
    for i, coin_type in enumerate(coin_types, 1):
        print(f"{i}. {coin_type['name']}")
    print(f"{len(coin_types) + 1}. Add New Coin Type")

    while True:
        try:
            type_choice = int(input("Select coin type: "))
            if 1 <= type_choice <= len(coin_types):
                coin_type_id = coin_types[type_choice - 1]["id"]
                break
            elif type_choice == len(coin_types) + 1:
                new_type_name = input("Enter new coin type name: ")
                coin_type_data = get_coin_type_input(new_type_name)
                coin_type_id = save_coin_type_to_database(coin_type_data)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    coin.type_id = coin_type_id  # TODO: validate the inputs for coin data
    coin.year = input("Year: ")
    coin.mint_mark = input("Mint Mark: ")

    conditions = get_conditions()
    print("\nAvailable Conditions:")
    for i, condition in enumerate(conditions, 1):
        print(f"{i}. {condition['name']}")
    print(f"{len(conditions) + 1}. Add New Condition")

    while True:
        try:
            condition_choice = int(input("Select condition: "))
            if 1 <= condition_choice <= len(conditions):
                condition_id = conditions[condition_choice - 1]["id"]
                break
            elif condition_choice == len(conditions) + 1:
                new_condition_name = input(
                    "Enter new condition name using the Shelldon Scale (e.g. MS-65): "
                )
                condition_id = add_condition(new_condition_name)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    coin.condition_id = condition_id
    coin.quantity = input("Quantity: ")
    coin.value_estimate = input("Value Estimate: ")
    coin.acquired_from = input("Acquired From: ")
    coin.notes = input("Notes: ")

    return coin.to_dict()


def get_coin_type_input(new_type_name=None):
    """Get coin type input from the user."""
    coin_type = CoinType()
    coin_type.name = new_type_name
    if new_type_name is None:
        new_type_name = input("Enter new coin type name: ")
        coin_type.name = new_type_name
    else:
        print(f"Adding new information for {new_type_name}...")

    coin_type.denomination = input(
        "Enter coin type denomination: (e.g. 1 Dollar, 1 Cent) "
    )
    coin_type.country_id = input(
        "Enter coin type country ID: (e.g. 40 for CA, 235 for US) "
    )
    coin_type.metal = input("Enter coin type metal: (e.g. Silver, Copper, Nickel) ")

    return coin_type.to_dict()


def add_coin_type_page():
    """Add New Coin Type page."""
    print(get_page_header("Add New Coin Type"))
    coin_type_data = get_coin_type_input()
    coin_type_id = save_coin_type_to_database(coin_type_data)
    print(
        f"You have added {coin_type_data['name']} successfully with ID {coin_type_id}."
    )
    input("\nPress Enter to continue...")


def add_condition_page():
    """Add New Condition page."""
    print(get_page_header("Add New Condition"))
    new_condition_name = input(
        "Enter new condition name using the Shelldon Scale (e.g. MS-65): "
    )
    condition_id = add_condition(new_condition_name)
    print(f"You have added {new_condition_name} successfully with ID {condition_id}.")
    input("\nPress Enter to continue...")


def add_country_page():
    """Add New Country page."""
    print(get_page_header("Add New Country"))
    print("Add country functionality coming soon...")
    input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_page()
