"""Forms module for the Coin Tracker Database.

Handles all user input collection for coins, coin types, conditions, and countries.
Separated from pages.py to maintain clean separation between presentation and data input logic.
"""

from models.coin import Coin
from models.coin_type import CoinType
from models.condition import Condition
from models.country import Country
from database import (
    get_coin_by_id,
    get_coin_types,
    get_coin_type_by_id,
    save_coin_type_to_database,
    get_conditions,
    save_condition_to_database,
    get_country_id_by_code
)


class UserCancelledError(Exception):
    """Exception raised when user cancels an input operation."""

    def __init__(self):
        self.message = "User cancelled the operation"
        super().__init__(self.message)


def _input_with_quit_check(prompt: str, default: str = None) -> str:
    """Get input from user and check if they want to quit.

    Args:
        prompt: The prompt to display to the user
        default: Optional default value to show and use if user presses Enter

    Returns:
        The user's input string or default if provided and user pressed Enter

    Raises:
        UserCancelledError: If user enters 'quit'
    """
    # Show default in brackets if provided
    if default is not None:
        display_prompt = f"{prompt}[{default}]: "
    else:
        display_prompt = prompt

    user_input = input(display_prompt)

    if user_input.lower().strip() == "quit":
        raise UserCancelledError()

    # Return default if no input and default exists
    if not user_input and default is not None:
        return str(default)

    return user_input


def _collect_coin_data(existing_coin: Coin = None) -> dict:
    coin = existing_coin if existing_coin else Coin()

    def get_existing_coin_data(attr: str) -> dict:
        return getattr(existing_coin, attr, None) if existing_coin else None

    # TODO: validate the inputs for coin data
    coin.type_id = _select_coin_type(get_existing_coin_data("type_id"))
    print(f"Coin Type ID: {coin.type_id}")
    coin.year = int(_input_with_quit_check(
        "Year: ", get_existing_coin_data("year")))
    coin.mint_mark = _input_with_quit_check(
        "Mint Mark: ", get_existing_coin_data("mint_mark") or "-")
    coin.condition_id = _select_condition(
        get_existing_coin_data("condition_id"))
    coin.quantity = int(_input_with_quit_check(
        "Quantity: ", get_existing_coin_data("quantity")))
    coin.value_estimate = float(_input_with_quit_check(
        "Value Estimate: ", get_existing_coin_data("value_estimate")))
    coin.acquired_from = _input_with_quit_check(
        "Acquired From: ", get_existing_coin_data("acquired_from"))
    coin.notes = _input_with_quit_check(
        "Notes: ", get_existing_coin_data("notes"))

    return coin.to_dict()


def _select_coin_type(selected_coin_type_id: int = None) -> int:
    coin_types = get_coin_types()
    print("Available Coin Types:")
    for i, coin_type in enumerate(coin_types, 1):
        print(f"{i}. {coin_type['name']}")
    print("--------------------")
    print(f"{len(coin_types) + 1}. Add New Coin Type\n")

    # Convert database ID to list position for display
    default_position = None
    if selected_coin_type_id:
        for i, coin_type in enumerate(coin_types, 1):
            if coin_type['id'] == selected_coin_type_id:
                default_position = i
                break

    while True:
        try:
            type_choice = _input_with_quit_check(
                "Select coin type: ", default_position)
            if type_choice is None:
                break
            type_choice_int = int(type_choice)

            if 1 <= type_choice_int <= len(coin_types):
                coin_type_id = coin_types[type_choice_int - 1]["id"]
                break
            elif type_choice_int == len(coin_types) + 1:
                coin_type_data = get_coin_type_input()
                coin_type_id = save_coin_type_to_database(coin_type_data)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    return coin_type_id


def _select_condition(selected_condition_id: int = None) -> int:
    conditions = get_conditions()
    print("Available Conditions:")
    for i, condition in enumerate(conditions, 1):
        print(f"{i}. {condition['name']}: {condition['description']}")
    print("---------------------")
    print(f"{len(conditions) + 1}. Add New Condition\n")

    # Convert database ID to list position for display
    default_position = None
    if selected_condition_id:
        for i, condition in enumerate(conditions, 1):
            if condition['id'] == selected_condition_id:
                default_position = i
                break

    while True:
        try:
            condition_choice = _input_with_quit_check(
                "Select condition: ", default_position)
            if condition_choice is None:
                break
            condition_choice_int = int(condition_choice)

            if 1 <= condition_choice_int <= len(conditions):
                condition_id = conditions[condition_choice_int - 1]["id"]
                break
            elif condition_choice_int == len(conditions) + 1:
                condition_data = get_condition_input()
                condition_id = save_condition_to_database(condition_data)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    return condition_id


def get_coin_input() -> dict:
    """Get coin input from the user."""
    coin_data = _collect_coin_data()

    return coin_data


def get_coin_type_input() -> dict:
    """Get coin type input from the user."""
    coin_type = CoinType()
    new_type_name = _input_with_quit_check("Enter new coin type name: ")
    coin_type.name = new_type_name
    coin_type.denomination = _input_with_quit_check(
        "Enter coin type denomination: (e.g. 1 Dollar, 1 Cent) "
    )
    country_code = _input_with_quit_check(
        "Enter coin type country code: (e.g. CA, US, etc...) "
    )
    coin_type.country_id = get_country_id_by_code(country_code)
    coin_type.metal = _input_with_quit_check(
        "Enter coin type metal: (e.g. Silver, Copper, Nickel) ")

    return coin_type.to_dict()


def get_condition_input() -> dict:
    """Get condition input from the user."""
    condition = Condition()
    new_condition_name = _input_with_quit_check(
        "Enter new condition name using the Shelldon Scale (e.g. MS-65): ")
    condition.name = new_condition_name
    condition.description = _input_with_quit_check(
        "Enter condition description: (e.g. Mint State 65, Very Fine 20) ")

    return condition.to_dict()


def get_country_input() -> dict:
    """Get country input from the user."""
    country = Country()
    new_country_name = _input_with_quit_check("Enter new country name: ")
    country.name = new_country_name
    country.country_code = _input_with_quit_check("Enter new country code: ")

    return country.to_dict()


def get_updated_coin_input(coin_id: str) -> dict:
    """Get updated coin input from the user with current values as defaults."""
    selected_coin = get_coin_by_id(coin_id)
    coin = Coin(**selected_coin)

    print("\n** Press Enter to keep current value, or type new value **\n")

    coin_data = _collect_coin_data(coin)

    return coin_data


def get_updated_coin_type_input(coin_type_id: str) -> dict:
    """Get updated coin type input from the user with current values as defaults."""
    selected_coin_type = get_coin_type_by_id(coin_type_id)
    coin_type = CoinType(**selected_coin_type)

    print("\n** Press Enter to keep current value, or type new value **\n")

    coin_type_data = get_coin_type_input()
    coin_type_id = save_coin_type_to_database(coin_type_data)

    return coin_type.to_dict()
