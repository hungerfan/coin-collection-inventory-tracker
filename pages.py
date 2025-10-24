"""Pages module for the Coin Tracker Database."""
from forms import (
    get_coin_input,
    get_coin_type_input,
    get_condition_input,
    get_country_input,
    get_updated_coin_input,
    get_updated_coin_type_input,
    UserCancelledError
)
from database import (
    get_data_count,
    get_coins_with_details,
    save_coin_to_database,
    get_coin_types,
    save_coin_type_to_database,
    save_condition_to_database,
    save_country_to_database,
    update_coin_in_database,
    update_coin_type_in_database
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


def _success_message(name: str, uid: int) -> str:
    """Get the success message."""
    return f"You have added {name} successfully with ID {uid}."


def main_page():
    """Main Page function."""
    while True:
        print(_get_page_header("Main Menu"))
        coin_count = get_data_count()

        _display_main_menu(coin_count)
        choice = input("Enter your choice: ")

        if not _handle_main_menu_choice(choice, coin_count > 0):
            break


def _display_main_menu(coin_count: int):
    """Display the main menu options."""
    coin_text = f"There is {coin_count} coin" if coin_count == 1 else f"There are {coin_count} coins"
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
        print("** Invalid choice **\n")

    return True


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
            print("** Invalid choice **\n")


def view_coins_page():
    """View Coins page."""
    print(_get_page_header("View Coins"))

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

    coin_row_template = "{id:<4} {type:<20} {year:<6} {mint:<6} {cond:<12} " \
        "{qty:<4} {val:<8} {country:<12} {received_from:<15}"

    for coin in coins:
        # Format the data for display
        coin_id = str(coin["id"])
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
        coin_type = coin_type[:18] + ".." if len(coin_type) > 20 else coin_type
        condition = condition[:10] + ".." if len(condition) > 12 else condition
        country = country[:10] + ".." if len(country) > 12 else country
        received_from = (
            received_from[:13] +
            ".." if len(received_from) > 15 else received_from
        )

        print(
            coin_row_template.format(
                id=coin_id,
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

    input("\nPress Enter to continue...")


def add_coin_page():
    """Add New Coin page."""
    print(_get_page_header("Add New Coin", show_quit_message=True))

    try:
        coin_data = get_coin_input()
        save_coin_to_database(coin_data)
        print("Coin added successfully!\n")
    except UserCancelledError:
        print("\n** Operation cancelled. Returning to menu. **")
        input("\nPress Enter to continue...")


def add_coin_type_page():
    """Add New Coin Type page."""
    print(_get_page_header("Add New Coin Type", show_quit_message=True))

    try:
        coin_type_data = get_coin_type_input()
        coin_type_id = save_coin_type_to_database(coin_type_data)
        print(_success_message(name=coin_type_data['name'], uid=coin_type_id))
        input("\nPress Enter to continue...")
    except UserCancelledError:
        print("\n** Operation cancelled. Returning to menu. **")
        input("\nPress Enter to continue...")


def add_condition_page():
    """Add New Condition page."""
    print(_get_page_header("Add New Condition"))

    try:
        condition_data = get_condition_input()
        condition_id = save_condition_to_database(condition_data)
        print(_success_message(name=condition_data['name'], uid=condition_id))
        input("\nPress Enter to continue...")
    except UserCancelledError:
        print("\n** Operation cancelled. Returning to menu. **")
        input("\nPress Enter to continue...")


def add_country_page():
    """Add New Country page."""
    print(_get_page_header("Add New Country"))

    try:
        while True:
            country_data = get_country_input()
            country_id = save_country_to_database(country_data)
            if country_id is not None:
                break
            else:
                print("Country code already exists. Please try again.")

        print(_success_message(name=country_data['name'], uid=country_id))
        input("\nPress Enter to continue...")
    except UserCancelledError:
        print("\n** Operation cancelled. Returning to menu. **")
        input("\nPress Enter to continue...")


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
            print("** Invalid choice **\n")


def update_coin_page():
    """Update Coins page."""
    print(_get_page_header("Update Coins"))

    show_list = True  # Flag to control when to display the coin list

    while True:
        # Display coins list when needed (first time or after cancellation)
        if show_list:
            # Fetch fresh data from database
            coins = get_coins_with_details()

            if not coins:
                print("No coins found in the database.")
                input("\nPress Enter to continue...")
                return

            # Display coins in a formatted table
            print(
                f"{'':<3} {'':<1} {'Coin Type':<20} {'Year':<6} {'Mint':<6} {'Condition':<12} "
                f"{'Qty':<4} {'Value':<8} {'Country':<12} {'Acquired From':<15}"
            )
            print("-" * 120)

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

            print(coin_row_template.format(
                count=cnt + 1,
                dash='-',
                type='Back to Update Menu',
                year='',
                mint='',
                cond='',
                qty='',
                val='',
                country='',  # -us,
                received_from=''
            ))

            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for coin to update: ")
            if choice == str(cnt + 1):
                return

            updated_coin_data = get_updated_coin_input(
                str(coins[int(choice) - 1]["id"]))

            update_coin_in_database(updated_coin_data)

            print("Coin updated successfully!\n")
            input("Press Enter to continue...")

            show_list = True  # Show list again after successful update
        except ValueError:
            print("** Invalid choice **")
        except IndexError:
            print("** Invalid choice **")
        except UserCancelledError:
            print("\n** Operation cancelled. Returning to coin list. **\n")
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

            if not coin_types:
                print("No coin types found in the database.")
                input("\nPress Enter to continue...")
                return

            # Display coin types in a formatted table
            print(
                f"{'':<3} {'':<1} {'Coin Type':<20} {'Denomination':<15} {'Country':<12} "
                f"{'Metal':<10}"
            )
            print("-" * 120)

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

            show_list = False  # Don't show again unless needed

        try:
            choice = input("\nEnter number for coin type to update: ")
            if choice == str(cnt + 1):
                return

            updated_coin_type_data = get_updated_coin_type_input(
                str(coin_types[int(choice) - 1]["id"]))

            update_coin_type_in_database(updated_coin_type_data)

            print("Coin type updated successfully!\n")
            input("Press Enter to continue...")

            show_list = True  # Show list again after successful update
        except ValueError:
            print("** Invalid choice **")
        except IndexError:
            print("** Invalid choice **")
        except UserCancelledError:
            print("\n** Operation cancelled. Returning to coin type list. **\n")
            show_list = True  # Redisplay the list after cancellation


def update_condition_page():
    """Update Conditions page."""
    print(_get_page_header("Update Conditions"))
    print("Update conditions functionality coming soon...")
    input("\nPress Enter to continue...")


def update_country_page():
    """Update Countries page."""
    print(_get_page_header("Update Countries"))
    print("Update countries functionality coming soon...")
    input("\nPress Enter to continue...")


def delete_data_page():
    """Delete Data page."""
    print(_get_page_header("Delete Data"))
    print("Delete data functionality coming soon...")
    input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_page()
