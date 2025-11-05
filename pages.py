"""Pages module for the Coin Tracker Database.

Contains all page/view functions for the terminal-based UI including
main menu, insert, update, delete, and view operations.
"""

from typing import List, Dict, Any, Callable, Optional
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
    get_coin_by_id,
    get_coins_with_details,
    save_coin_to_database,
    get_coin_types,
    get_coin_type_by_id,
    save_coin_type_to_database,
    get_conditions,
    get_condition_by_id,
    save_condition_to_database,
    get_countries,
    get_country_by_id,
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
from constants import (
    TABLE_WIDTH,
    MSG_ENTER_CHOICE,
    MSG_INVALID_CHOICE,
    MSG_OPERATION_CANCELLED,
    MSG_PRESS_ENTER_PROMPT,
    MSG_QUIT_INSTRUCTION
)


# ============================================================================
# MESSAGE HELPER FUNCTIONS
# ============================================================================

def _get_page_header(page_name: str, show_quit_message: bool = False) -> str:
    """Generate page header with title and optional quit message.

    Args:
        page_name: Name of the page to display
        show_quit_message: Whether to show quit instructions

    Returns:
        Formatted header string
    """
    page_title = f"Coin Tracker Database - {page_name}"
    page_title_length = len(page_title)
    page_header_border = "-" * page_title_length

    page_header = f"\n{page_header_border}\n{page_title}\n{page_header_border}\n"
    if show_quit_message:
        page_header += MSG_QUIT_INSTRUCTION

    return page_header


def _success_add_message(name: str, uid: int) -> str:
    """Generate success message for add operations."""
    return f"** You have added {name} successfully with ID {uid}. **\n"


def _success_update_message(name: str) -> str:
    """Generate success message for update operations."""
    return f"** The {name} has been updated successfully. **\n"


def _success_delete_message(name: str) -> str:
    """Generate success message for delete operations."""
    return f"** You have deleted the {name} successfully. **\n"


def _failure_message(name: str) -> str:
    """Generate failure message for operations."""
    return f"\n** Failed to {name}. **\n"


def _invalid_choice_message() -> str:
    """Get the invalid choice message."""
    return MSG_INVALID_CHOICE


def _operation_cancelled_message() -> str:
    """Get the operation cancelled message."""
    return MSG_OPERATION_CANCELLED


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def _display_main_menu(coin_count: int) -> None:
    """Display the main menu options.

    Args:
        coin_count: Number of coins in the database
    """
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
    """Handle user menu choice.

    Args:
        choice: User's menu selection
        has_coins: Whether database has coins

    Returns:
        True to continue, False to exit
    """
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


def _handle_list_operation(
    page_name: str,
    get_items_func: Callable,
    display_func: Callable,
    operation_func: Callable,
    prompt: str,
    success_msg: str,
    failure_msg: str
) -> None:
    """Generic handler for list-based operations (update/delete).

    Args:
        page_name: Name of the page to display
        get_items_func: Function to fetch list of items from database
        display_func: Function to display the items list
        operation_func: Function to perform the operation (update/delete)
        prompt: User prompt for selecting an item
        success_msg: Message to display on success
        failure_msg: Message to display on failure
    """
    print(_get_page_header(page_name))
    show_list = True

    while True:
        if show_list:
            items = get_items_func()
            display_func(items)
            show_list = False

        try:
            choice = input(f"\n{prompt}: ")
            if choice == str(len(items) + 1):
                return

            result = operation_func(str(items[int(choice) - 1]["id"]))
            if result is not None and result >= 0:
                if result == 0:
                    print("No changes were made.")
                else:
                    print(success_msg)
            else:
                print(failure_msg)

            input(MSG_PRESS_ENTER_PROMPT)
            show_list = True
        except (ValueError, IndexError):
            print(_invalid_choice_message())
        except UserCancelledError:
            print(_operation_cancelled_message())
            show_list = True
        except Exception as e:
            print(f"Unexpected error: {e}")
            show_list = True


def _display_coins_list(coins: List[Dict[str, Any]], page_name: Optional[str] = None) -> None:
    """Display the coins list in formatted table.

    Args:
        coins: List of coin dictionaries
        page_name: Optional page name to show back button
    """
    if not coins:
        print("No coins found in the database.\n")
        input(MSG_PRESS_ENTER_PROMPT)
        return

    # Display coins in a formatted table
    print(
        f"{'':<3} {'':<1} {'Coin Type':<20} {'Year':<6} {'Mint':<6} {'Condition':<12} "
        f"{'Qty':<4} {'Value':<8} {'Country':<12} {'Acquired From':<15}"
    )
    print("-" * TABLE_WIDTH)

    coin_row_template = (
        "{count:>3} {dash:<1} {type:<20} {year:<6} {mint:<6} {cond:<12} "
        "{qty:<4} {val:<8} {country:<12} {received_from:<15}"
    )

    cnt = 0
    estimated_value = 0

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
        estimated_value += float(coin['value_estimate'])

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

    melt_value = 35.00 * cnt

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
    else:
        print(f"\nTotal Estimated Value: ${estimated_value:.2f}")
        print(f"Total Melt Value: ${melt_value:.2f}", end="")

    print("\n")


def _display_coin_types_list(coin_types: List[Dict[str, Any]]) -> None:
    """Display the coin types list in formatted table.

    Args:
        coin_types: List of coin type dictionaries
    """
    if not coin_types:
        print("No coin types found in the database.\n")
        input(MSG_PRESS_ENTER_PROMPT)
        return

    # Display coin types in a formatted table
    print(
        f"{'':<3} {'':<1} {'Coin Type':<20} {'Denomination':<15} {'Country':<12} "
        f"{'Metal':<10}"
    )
    print("-" * TABLE_WIDTH)

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


def _display_conditions_list(conditions: List[Dict[str, Any]]) -> None:
    """Display the conditions list in formatted table.

    Args:
        conditions: List of condition dictionaries
    """
    if not conditions:
        print("No conditions found in the database.\n")
        input(MSG_PRESS_ENTER_PROMPT)
        return

    print(f"{'':<3} {'':<1} {'Condition':<10} {'Description':<75}")
    print("-" * TABLE_WIDTH)

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


def _display_countries_list(countries: List[Dict[str, Any]]) -> None:
    """Display the countries list in formatted table.

    Args:
        countries: List of country dictionaries
    """
    if not countries:
        print("No countries found in the database.\n")
        input(MSG_PRESS_ENTER_PROMPT)
        return

    print(f"{'':<3} {'':<1} {'Country Code':<4} {'Country':<50}")
    print("-" * TABLE_WIDTH)

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


# ============================================================================
# MAIN PAGE FUNCTIONS
# ============================================================================

def main_page() -> None:
    """Main Page function - entry point for the application."""
    while True:
        print(_get_page_header("Main Menu"))
        coin_count = get_data_count()

        _display_main_menu(coin_count)
        choice = input(MSG_ENTER_CHOICE)

        if not _handle_main_menu_choice(choice, coin_count > 0):
            break


def insert_data_page() -> None:
    """Insert Data page - allows adding new records."""
    while True:
        print(_get_page_header("Insert Data"))

        print("OPTIONS:")
        print("  1 - Add New Coin")
        print("  2 - Add New Coin Type")
        print("  3 - Add New Condition")
        print("  4 - Add New Country")
        print("  5 - Back to Main Menu\n")

        choice = input(MSG_ENTER_CHOICE)

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


def view_coins_page() -> None:
    """View Coins page - displays all coins in the database."""
    print(_get_page_header("View Coins"))

    coins = get_coins_with_details()

    _display_coins_list(coins)

    input(MSG_PRESS_ENTER_PROMPT)


# ============================================================================
# ADD PAGES
# ============================================================================

def add_coin_page() -> None:
    """Add New Coin page - collects and saves new coin data."""
    print(_get_page_header("Add New Coin", show_quit_message=True))

    try:
        coin_data = get_coin_input()
        coin_id = save_coin_to_database(coin_data)
        if isinstance(coin_id, int):
            print(_success_add_message(
                name="a new coin", uid=coin_id))
        else:
            print(_failure_message("add a new coin"))

        input(MSG_PRESS_ENTER_PROMPT)
    except UserCancelledError:
        print(_operation_cancelled_message())
        input(MSG_PRESS_ENTER_PROMPT)


def add_coin_type_page() -> None:
    """Add New Coin Type page - collects and saves new coin type data."""
    print(_get_page_header("Add New Coin Type", show_quit_message=True))

    try:
        coin_type_data = get_coin_type_input()
        coin_type_id = save_coin_type_to_database(coin_type_data)
        if isinstance(coin_type_id, int):
            print(_success_add_message(
                name=coin_type_data['name'], uid=coin_type_id))
        else:
            print(_failure_message("add a new coin type"))

        input(MSG_PRESS_ENTER_PROMPT)
    except UserCancelledError:
        print(_operation_cancelled_message())
        input(MSG_PRESS_ENTER_PROMPT)


def add_condition_page() -> None:
    """Add New Condition page - collects and saves new condition data."""
    print(_get_page_header("Add New Condition", show_quit_message=True))

    try:
        condition_data = get_condition_input()
        condition_id = save_condition_to_database(condition_data)
        if isinstance(condition_id, int):
            print(_success_add_message(
                name=condition_data['name'], uid=condition_id))
        else:
            print(_failure_message("add a new condition"))

        input(MSG_PRESS_ENTER_PROMPT)
    except UserCancelledError:
        print(_operation_cancelled_message())
        input(MSG_PRESS_ENTER_PROMPT)


def add_country_page() -> None:
    """Add New Country page - collects and saves new country data."""
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

        input(MSG_PRESS_ENTER_PROMPT)
    except UserCancelledError:
        print(_operation_cancelled_message())
        input(MSG_PRESS_ENTER_PROMPT)


# ============================================================================
# UPDATE PAGES
# ============================================================================

def update_data_page() -> None:
    """Update Data page - menu for selecting what to update."""
    while True:
        print(_get_page_header("Update Data"))

        print("OPTIONS:")
        print("  1 - Update Coins")
        print("  2 - Update Coin Types")
        print("  3 - Update Conditions")
        print("  4 - Update Countries")
        print("  5 - Back to Main Menu\n")

        choice = input(MSG_ENTER_CHOICE)

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


def update_coin_page() -> None:
    """Update Coins page - select and update coin records."""
    def update_coin_operation(coin_id: str) -> Optional[int]:
        updated_data = get_updated_coin_input(coin_id)
        if updated_data:
            return update_coin_in_database(updated_data)
        return None

    _handle_list_operation(
        page_name="Update Coins",
        get_items_func=get_coins_with_details,
        display_func=lambda coins: _display_coins_list(coins, "Update Coins"),
        operation_func=update_coin_operation,
        prompt="Enter number for the coin to update",
        success_msg=_success_update_message("coin"),
        failure_msg=_failure_message("update a coin")
    )


def update_coin_type_page() -> None:
    """Update Coin Types page - select and update coin type records."""
    def update_coin_type_operation(coin_type_id: str) -> Optional[int]:
        updated_data = get_updated_coin_type_input(coin_type_id)
        if updated_data:
            return update_coin_type_in_database(updated_data)
        return None

    _handle_list_operation(
        page_name="Update Coin Types",
        get_items_func=get_coin_types,
        display_func=_display_coin_types_list,
        operation_func=update_coin_type_operation,
        prompt="Enter number for the coin type to update",
        success_msg=_success_update_message("coin type"),
        failure_msg=_failure_message("update a coin type")
    )


def update_condition_page() -> None:
    """Update Conditions page - select and update condition records."""
    def update_condition_operation(condition_id: str) -> Optional[int]:
        updated_data = get_updated_condition_input(condition_id)
        if updated_data:
            return update_condition_in_database(updated_data)
        return None

    _handle_list_operation(
        page_name="Update Conditions",
        get_items_func=get_conditions,
        display_func=_display_conditions_list,
        operation_func=update_condition_operation,
        prompt="Enter number for the condition to update",
        success_msg=_success_update_message("condition"),
        failure_msg=_failure_message("update a condition")
    )


def update_country_page() -> None:
    """Update Countries page - select and update country records."""
    def update_country_operation(country_id: str) -> Optional[int]:
        updated_data = get_updated_country_input(country_id)
        if updated_data:
            return update_country_in_database(updated_data)
        return None

    _handle_list_operation(
        page_name="Update Countries",
        get_items_func=get_countries,
        display_func=_display_countries_list,
        operation_func=update_country_operation,
        prompt="Enter number for the country to update",
        success_msg=_success_update_message("country"),
        failure_msg=_failure_message("update a country")
    )


# ============================================================================
# DELETE PAGES
# ============================================================================

def delete_data_page() -> None:
    """Delete Data page - menu for selecting what to delete."""
    while True:
        print(_get_page_header("Delete Data"))

        print("OPTIONS:")
        print("  1 - Delete Coins")
        print("  2 - Delete Coin Types")
        print("  3 - Delete Conditions")
        print("  4 - Delete Countries")
        print("  5 - Back to Main Menu\n")

        choice = input(MSG_ENTER_CHOICE)

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
            print(_invalid_choice_message())


def delete_coin_page() -> None:
    """Delete Coins page - select and delete coin records."""
    def delete_coin_operation(coin_id: str) -> Optional[int]:
        return delete_coin_from_database(coin_id) if confirm_delete_coin_input(
            get_coin_by_id(coin_id)) else None

    _handle_list_operation(
        page_name="Delete Coins",
        get_items_func=get_coins_with_details,
        display_func=lambda coins: _display_coins_list(coins, "Delete Coins"),
        operation_func=delete_coin_operation,
        prompt="Enter number for the coin to delete",
        success_msg=_success_delete_message("coin"),
        failure_msg=_failure_message("delete a coin")
    )


def delete_coin_type_page() -> None:
    """Delete Coin Types page - select and delete coin type records."""
    def delete_coin_type_operation(coin_type_id: str) -> Optional[int]:
        return delete_coin_type_from_database(coin_type_id) if confirm_delete_coin_type_input(
            get_coin_type_by_id(coin_type_id)) else None

    _handle_list_operation(
        page_name="Delete Coin Types",
        get_items_func=get_coin_types,
        display_func=_display_coin_types_list,
        operation_func=delete_coin_type_operation,
        prompt="Enter number for the coin type to delete",
        success_msg=_success_delete_message("coin type"),
        failure_msg=_failure_message("delete a coin type")
    )


def delete_condition_page() -> None:
    """Delete Conditions page - select and delete condition records."""
    def delete_condition_operation(condition_id: str) -> Optional[int]:
        return delete_condition_from_database(condition_id) if confirm_delete_condition_input(
            get_condition_by_id(condition_id)) else None

    _handle_list_operation(
        page_name="Delete Conditions",
        get_items_func=get_conditions,
        display_func=_display_conditions_list,
        operation_func=delete_condition_operation,
        prompt="Enter number for the condition to delete",
        success_msg=_success_delete_message("condition"),
        failure_msg=_failure_message("delete a condition")
    )


def delete_country_page() -> None:
    """Delete Countries page - select and delete country records."""
    def delete_country_operation(country_id: str) -> Optional[int]:
        return delete_country_from_database(country_id) if confirm_delete_country_input(
            get_country_by_id(country_id)) else None

    _handle_list_operation(
        page_name="Delete Countries",
        get_items_func=get_countries,
        display_func=_display_countries_list,
        operation_func=delete_country_operation,
        prompt="Enter number for the country to delete",
        success_msg=_success_delete_message("country"),
        failure_msg=_failure_message("delete a country")
    )


if __name__ == "__main__":
    main_page()
