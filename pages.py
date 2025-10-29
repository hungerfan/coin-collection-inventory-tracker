"""Pages module for the Coin Tracker Database."""
from forms import (
    get_coin_input,
    get_coin_type_input,
    get_condition_input,
    get_country_input,
    get_updated_coin_input,
    get_updated_coin_type_input,
    get_updated_condition_input,
    get_updated_country_input,
    confirm_delete_coin_input,
    confirm_delete_coin_type_input,
    confirm_delete_condition_input,
    confirm_delete_country_input,
    UserCancelledError
)
from database import (
    get_data_count,
    get_coins_with_details,
    save_coin_to_database,
    get_coin_types,
    save_coin_type_to_database,
    get_conditions,
    save_condition_to_database,
    get_countries,
    save_country_to_database,
    update_coin_in_database,
    update_coin_type_in_database,
    update_condition_in_database,
    update_country_in_database,
    delete_coin_from_database,
    delete_coin_type_from_database,
    delete_condition_from_database,
    delete_country_from_database
)


def _get_page_header(page_name: str, show_quit_message: bool = False) -> str:
    """Get the page header."""
    page_title = f"Coin Tracker Database - {page_name}"
    page_title_length = len(page_title)
    page_header_border = "-" * page_title_length

    page_header = f"\n{page_header_border}\n{page_title}\n{page_header_border}\n"
    if show_quit_message:
        page_header += "Enter 'quit' at any time to cancel the operation\n"

    return page_header


def _success_add_message(name: str, uid: int) -> str:
    """Get the success add message."""
    return f"** You have added {name} successfully with ID {uid}. **\n"


def _success_update_message(name: str) -> str:
    """Get the success update message."""
    return f"** The {name} has been updated successfully. **\n"


def _success_delete_message(name: str) -> str:
    """Get the success delete message."""
    return f"** You have deleted the {name} successfully. **\n"


def _failure_message(name: str) -> str:
    """Get the failure message."""
    return f"\n** Failed to {name}. **\n"


def _invalid_choice_message() -> str:
    """Get the invalid choice message."""
    return "\n** Invalid choice. Please try again. **\n"


def _operation_cancelled_message() -> str:
    """Get the operation cancelled message."""
    return "\n** Operation cancelled. Returning to menu. **\n"


def _display_main_menu(coin_count: int):
    """Display the main menu options."""
    coin_text = f"There is {coin_count} coin" if coin_count == 1 else \
        f"There are {coin_count} coins"
    if coin_count == 0:
        coin_text = "There are no coins"
    print(f"{coin_text} in the database.\n")

    print("OPTIONS:")
    if coin_count > 0:
        print("  1 - View Coins")
        print("  2 - Insert Data")
        print("  3 - Update Data")
        print("  4 - Delete Data")
        print("  5 - Exit\n")
    else:
        print("  1 - Insert Data")
        print("  2 - Exit\n")


def _handle_main_menu_choice(choice: str, has_coins: bool) -> bool:
    """Handle user menu choice. Returns True to continue, False to exit."""
    if has_coins:
        menu_actions = {
            "1": view_coins_page,
            "2": insert_data_page,
            "3": update_data_page,
            "4": delete_data_page,
        }
        if choice == "5" or choice == "quit":
            print("Goodbye!")
            return False
    else:
        menu_actions = {"1": insert_data_page}
        if choice == "2" or choice == "quit":
            print("Goodbye!")
            return False

    if choice in menu_actions:
        menu_actions[choice]()
    else:
        print(_invalid_choice_message())

    return True


def _display_coins_list(coins, page_name: str = None):
    """Display the coins list."""
    if not coins:
        print("No coins found in the database.")
        input("\nPress Enter to continue...")
        return

    # Display coins in a formatted table
    print(
        f"{'':<3} {'':<1} {'Coin Type':<20} {'Year':<6} {'Mint':<6} {'Condition':<12} "
        f"{'Qty':<4} {'Value':<8} {'Country':<12} {'Acquired From':<15}"
    )
    print("-" * 100)

    coin_row_template = (
        "{count:>3} {dash:<1} {type:<20} {year:<6} {mint:<6} {cond:<12} "
        "{qty:<4} {val:<8} {country:<12} {received_from:<15}"
    )

    cnt = 0

    for i, coin in enumerate(coins, 0):
        # Format the data for display
        coin_type = coin["coin_type_name"] or "Unknown"
        year = str(coin["year"]) if coin["year"] else "N/A"
        mint_mark = coin["mint_mark"] or "-"
        condition = coin["condition_name"] or "Unknown"
        quantity = str(coin["quantity"]) if coin["quantity"] else "N/A"
        value = (
            f"${float(coin['value_estimate']):.2f}" if coin["value_estimate"] else "N/A"
        )
        country = coin["country_name"] or "Unknown"
        received_from = coin["acquired_from"] or "N/A"

        # Truncate long strings for better display
        coin_type = coin_type[:18] + \
            ".." if len(coin_type) > 20 else coin_type
        condition = condition[:10] + \
            ".." if len(condition) > 12 else condition
        country = country[:10] + ".." if len(country) > 12 else country
        received_from = (
            received_from[:13] +
            ".." if len(received_from) > 15 else received_from
        )

        cnt = i + 1

        print(
            coin_row_template.format(
                count=cnt,
                dash='-',
                type=coin_type,
                year=year,
                mint=mint_mark,
                cond=condition,
                qty=quantity,
                val=value,
                country=country,
                received_from=received_from
            )
        )

    if page_name is not None:
        print(coin_row_template.format(
            count=cnt + 1,
            dash='-',
            type='Back to Update Menu',
            year='',
            mint='',
            cond='',
            qty='',
            val='',
            country='',
            received_from=''
        ))


def _display_coin_types_list(coin_types):
    """Display the coin types list."""
    if not coin_types:
        print("No coin types found in the database.")
        input("\nPress Enter to continue...")
        return

    # Display coin types in a formatted table
    print(
        f"{'':<3} {'':<1} {'Coin Type':<20} {'Denomination':<15} {'Country':<12} "
        f"{'Metal':<10}"
    )
    print("-" * 100)

    coin_type_row_template = (
        "{count:>3} {dash:<1} {type:<20} {denom:<15} {country:<12} {metal:<10}"
    )
    cnt = 0

    for i, coin_type in enumerate(coin_types, 0):
        # Format the data for display
        coin_type_name = coin_type["name"] or "Unknown"
        denomination = coin_type["denomination"] or "N/A"
        country = coin_type["country_name"] or "Unknown"
        metal = coin_type["metal"] or "N/A"

        # Truncate long strings for better display
        coin_type_name = coin_type_name[:18] + \
            ".." if len(coin_type_name) > 20 else coin_type_name
        denomination = denomination[:15] + \
            ".." if len(denomination) > 15 else denomination
        country = country[:10] + ".." if len(country) > 12 else country
        metal = metal[:10] + ".." if len(metal) > 10 else metal

        cnt = i + 1

        print(
            coin_type_row_template.format(
                count=cnt,
                dash='-',
                type=coin_type_name,
                denom=denomination,
                country=country,
                metal=metal
            )
        )

    print(coin_type_row_template.format(
        count=cnt + 1,
        dash='-',
        type='Back to Update Menu',
        denom='',
        country='',
        metal=''
    ))


def _display_conditions_list(conditions):
    """Display the conditions list."""
    if not conditions:
        print("No conditions found in the database.")
        input("\nPress Enter to continue...")
        return

    print(f"{'':<3} {'':<1} {'Condition':<10} {'Description':<75}")
    print("-" * 100)

    condition_row_template = (
        "{count:>3} {dash:<1} {type:<10} {description:<75}"
    )
    cnt = 0

    for i, condition in enumerate(conditions, 0):
        # Format the data for display
        condition_name = condition["name"] or "Unknown"
        description = condition["description"] or "N/A"

        # Truncate long strings for better display
        condition_name = condition_name[:10] + \
            ".." if len(condition_name) > 10 else condition_name
        description = description[:75] + \
            ".." if len(description) > 75 else description

        cnt = i + 1

        print(
            condition_row_template.format(
                count=cnt,
                dash='-',
                type=condition_name,
                description=description
            )
        )

    print(condition_row_template.format(
        count=cnt + 1,
        dash='-',
        type='Back to Update Menu',
        description=''
    ))


def _display_countries_list(countries):
    """Display the countries list."""
    if not countries:
        print("No countries found in the database.")
        input("\nPress Enter to continue...")
        return

    print(f"{'':<3} {'':<1} {'Country Code':<4} {'Country':<50}")
    print("-" * 100)

    country_row_template = (
        "{count:>3} {dash:<1} {country_code:<4} {country:<50}"
    )
    cnt = 0

    for i, country in enumerate(countries, 0):
        # Format the data for display
        country_code = country["country_code"] or "N/A"
        country_name = country["name"] or "Unknown"
        # Truncate long strings for better display
        country_code = country_code[:4] + \
            ".." if len(country_code) > 4 else country_code
        country_name = country_name[:50] + \
            ".." if len(country_name) > 50 else country_name

        cnt = i + 1

        print(
            country_row_template.format(
                count=cnt,
                dash='-',
                country_code=country_code,
                country=country_name
            )
        )

    print(country_row_template.format(
        count=cnt + 1,
        dash='-',
        country_code='',
        country='Back to Update Menu'
    ))


def main_page():
    """Main Page function."""
    while True:
        print(_get_page_header("Main Menu"))
        coin_count = get_data_count()

        _display_main_menu(coin_count)
        choice = input("Enter your choice: ")

        if not _handle_main_menu_choice(choice, coin_count > 0):
            break


def insert_data_page():
    """Insert Data page."""
    while True:
        print(_get_page_header("Insert Data"))

        print("OPTIONS:")
        print("  1 - Add New Coin")
        print("  2 - Add New Coin Type")
        print("  3 - Add New Condition")
        print("  4 - Add New Country")
        print("  5 - Back to Main Menu\n")

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
            print(_invalid_choice_message())


def view_coins_page():
    """View Coins page."""
    print(_get_page_header("View Coins"))

    coins = get_coins_with_details()

    _display_coins_list(coins)

    input("\nPress Enter to continue...")


def add_coin_page():
    """Add New Coin page."""
    print(_get_page_header("Add New Coin", show_quit_message=True))

    try:
        coin_data = get_coin_input()
        coin_id = save_coin_to_database(coin_data)
        if isinstance(coin_id, int):
            print(_success_add_message(
                name="a new coin", uid=coin_id))
        else:
            print(_failure_message("add a new coin"))

        input("Press Enter to continue...\n")
    except UserCancelledError:
        print(_operation_cancelled_message())
        input("Press Enter to continue...\n")


def add_coin_type_page():
    """Add New Coin Type page."""
    print(_get_page_header("Add New Coin Type", show_quit_message=True))

    try:
        coin_type_data = get_coin_type_input()
        coin_type_id = save_coin_type_to_database(coin_type_data)
        if isinstance(coin_type_id, int):
            print(_success_add_message(
                name=coin_type_data['name'], uid=coin_type_id))
        else:
            print(_failure_message("add a new coin type"))

        input("Press Enter to continue...\n")
    except UserCancelledError:
        print(_operation_cancelled_message())
        input("Press Enter to continue...\n")


def add_condition_page():
    """Add New Condition page."""
    print(_get_page_header("Add New Condition", show_quit_message=True))

    try:
        condition_data = get_condition_input()
        condition_id = save_condition_to_database(condition_data)
        if isinstance(condition_id, int):
            print(_success_add_message(
                name=condition_data['name'], uid=condition_id))
        else:
            print(_failure_message("add a new condition"))

        input("Press Enter to continue...\n")
    except UserCancelledError:
        print(_operation_cancelled_message())
        input("Press Enter to continue...\n")


def add_country_page():
    """Add New Country page."""
    print(_get_page_header("Add New Country", show_quit_message=True))

    try:
        while True:
            country_data = get_country_input()
            country_id = save_country_to_database(country_data)
            if country_id is not None:
                break
            else:
                print("** Country code already exists. Please try again. **\n")

        if isinstance(country_id, int):
            print(_success_add_message(
                name=country_data['name'], uid=country_id))
        else:
            print(_failure_message("add a new country"))

        input("Press Enter to continue...\n")
    except UserCancelledError:
        print(_operation_cancelled_message())
        input("Press Enter to continue...\n")


def update_data_page():
    """Update Data page."""
    while True:
        print(_get_page_header("Update Data"))

        print("OPTIONS:")
        print("  1 - Update Coins")
        print("  2 - Update Coin Types")
        print("  3 - Update Conditions")
        print("  4 - Update Countries")
        print("  5 - Back to Main Menu\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            update_coin_page()
        elif choice == "2":
            update_coin_type_page()
        elif choice == "3":
            update_condition_page()
        elif choice == "4":
            update_country_page()
        elif choice == "5":
            break  # Go back to main menu
        else:
            print(_invalid_choice_message())


def update_coin_page():
    """Update Coins page."""
    page_name = "Update Coins"
    print(_get_page_header(page_name))

    show_list = True  # Flag to control when to display the coin list

    while True:
        # Display coins list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            coins = get_coins_with_details()
            _display_coins_list(coins, page_name=page_name)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for coin to update: ")
            if choice == str(len(coins) + 1):
                return

            updated_coin_data = get_updated_coin_input(
                str(coins[int(choice) - 1]["id"]))

            result = update_coin_in_database(updated_coin_data)
            if result:
                print(_success_update_message("coin"))
            else:
                print(_failure_message("update a coin"))

            input("Press Enter to continue...\n")

            show_list = True  # Show list again after successful update
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


def update_coin_type_page():
    """Update Coin Types page."""
    print(_get_page_header("Update Coin Types"))

    show_list = True

    while True:
        # Display coin types list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            coin_types = get_coin_types()
            _display_coin_types_list(coin_types)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for coin type to update: ")
            if choice == str(len(coin_types) + 1):
                return

            updated_coin_type_data = get_updated_coin_type_input(
                str(coin_types[int(choice) - 1]["id"]))

            result = update_coin_type_in_database(updated_coin_type_data)
            if result:
                print(_success_update_message("coin type"))
            else:
                print(_failure_message("update a coin type"))

            input("Press Enter to continue...\n")

            show_list = True  # Show list again after successful update
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


def update_condition_page():
    """Update Conditions page."""
    print(_get_page_header("Update Conditions"))

    show_list = True

    while True:
        # Display conditions list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            conditions = get_conditions()
            _display_conditions_list(conditions)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for condition to update: ")
            if choice == str(len(conditions) + 1):
                return

            updated_condition_data = get_updated_condition_input(
                str(conditions[int(choice) - 1]["id"]))

            result = update_condition_in_database(updated_condition_data)
            if result:
                print(_success_update_message("condition"))
            else:
                print(_failure_message("update a condition"))

            show_list = True  # Show list again after successful update
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


def update_country_page():
    """Update Countries page."""
    print(_get_page_header("Update Countries"))

    show_list = True

    while True:
        # Display coin conditions in a formatted table
        if show_list:
            # Fetch fresh data from database
            countries = get_countries()
            _display_countries_list(countries)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for country to update: ")
            if choice == str(len(countries) + 1):
                return

            updated_country_data = get_updated_country_input(
                str(countries[int(choice) - 1]["id"]))

            result = update_country_in_database(updated_country_data)
            if result:
                print(_success_update_message("country"))
            else:
                print(_failure_message("update a country"))

            input("Press Enter to continue...\n")

            show_list = True  # Show list again after successful update
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


def delete_data_page():
    """Delete Data page."""
    while True:
        print(_get_page_header("Delete Data"))

        print("OPTIONS:")
        print("  1 - Delete Coins")
        print("  2 - Delete Coin Types")
        print("  3 - Delete Conditions")
        print("  4 - Delete Countries")
        print("  5 - Back to Main Menu\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            delete_coin_page()
        elif choice == "2":
            delete_coin_type_page()
        elif choice == "3":
            delete_condition_page()
        elif choice == "4":
            delete_country_page()
        elif choice == "5":
            break  # Go back to main menu
        else:
            print("** Invalid choice **\n")


def delete_coin_page():
    """Delete Coins page."""
    page_name = "Delete Coins"
    print(_get_page_header(page_name))

    show_list = True  # Flag to control when to display the coin list

    while True:
        # Display coins list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            coins = get_coins_with_details()
            _display_coins_list(coins, page_name=page_name)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for the coin to delete: ")
            if choice == str(len(coins) + 1):
                return

            confirm_delete_coin_input(coins[int(choice) - 1])
            # If we get here, user typed DELETE (otherwise UserCancelledError was raised)
            result = delete_coin_from_database(
                str(coins[int(choice) - 1]["id"]))
            if result:
                print(_success_delete_message("coin"))
            else:
                print(_failure_message("delete a coin"))

            input("Press Enter to continue...\n")

            show_list = True  # Redisplay the list after successful deletion
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


def delete_coin_type_page():
    """Delete Coin Types page."""
    print(_get_page_header("Delete Coin Types"))

    show_list = True  # Flag to control when to display the coin list

    while True:
        # Display coins list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            coin_types = get_coin_types()
            _display_coin_types_list(coin_types)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for the coin type to delete: ")
            if choice == str(len(coin_types) + 1):
                return

            confirm_delete_coin_type_input(coin_types[int(choice) - 1])
            # If we get here, user typed DELETE (otherwise UserCancelledError was raised)
            result = delete_coin_type_from_database(
                str(coin_types[int(choice) - 1]["id"]))
            if result:
                print(_success_delete_message("coin type"))
            else:
                print(_failure_message("delete a coin type"))

            input("Press Enter to continue...\n")

            show_list = True  # Redisplay the list after successful deletion
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


def delete_condition_page():
    """Delete Conditions page."""
    print(_get_page_header("Delete Conditions"))

    show_list = True  # Flag to control when to display the coin list

    while True:
        # Display conditions list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            conditions = get_conditions()
            _display_conditions_list(conditions)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for the condition to delete: ")
            if choice == str(len(conditions) + 1):
                return

            confirm_delete_condition_input(conditions[int(choice) - 1])
            # If we get here, user typed DELETE (otherwise UserCancelledError was raised)
            result = delete_condition_from_database(
                str(conditions[int(choice) - 1]["id"]))
            if result:
                print(_success_delete_message("condition"))
            else:
                print(_failure_message("delete a condition"))

            input("Press Enter to continue...\n")

            show_list = True  # Redisplay the list after successful deletion
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


def delete_country_page():
    """Delete Countries page."""
    print(_get_page_header("Delete Countries"))

    show_list = True

    while True:
        # Display countries list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            countries = get_countries()
            _display_countries_list(countries)
            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for the country to delete: ")
            if choice == str(len(countries) + 1):
                return

            confirm_delete_country_input(countries[int(choice) - 1])
            # If we get here, user typed DELETE (otherwise UserCancelledError was raised)
            result = delete_country_from_database(
                str(countries[int(choice) - 1]["id"]))
            if result:
                print(_success_delete_message("country"))
            else:
                print(_failure_message("delete a country"))

            input("Press Enter to continue...\n")

            show_list = True  # Redisplay the list after successful deletion
        except ValueError:
            print(_invalid_choice_message())
        except IndexError:
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True  # Redisplay the list after cancellation


if __name__ == "__main__":
    main_page()
