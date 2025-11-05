"""Forms module for the Coin Tracker Database.

Handles all user input collection for coins, coin types, conditions, and countries.
Separated from pages.py to maintain clean separation between presentation and
data input logic.
"""

from datetime import datetime
from typing import Optional, Dict, Any
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
    get_condition_by_id,
    save_condition_to_database,
    get_countries,
    get_country_id_by_code,
    get_country_by_id
)
from constants import DEFAULT_MINT_MARK, CONFIRM_DELETE_TEXT, MSG_INVALID_CHOICE


class UserCancelledError(Exception):
    """Exception raised when user cancels an input operation."""

    def __init__(self, message: str = "User cancelled the operation"):
        self.message = message
        super().__init__(self.message)


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def _validate_year(year_str: str) -> int:
    """Validate and return year.

    Args:
        year_str: Year as string

    Returns:
        Validated year as integer

    Raises:
        ValueError: If year is invalid
    """
    try:
        year = int(year_str)
        current_year = datetime.now().year
        if not (1 <= year <= current_year + 1):
            raise ValueError(f"Year must be between 1 and {current_year + 1}")
        return year
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Year must be a number") from e
        raise


def _validate_positive_int(value_str: str, field_name: str) -> int:
    """Validate positive integer.

    Args:
        value_str: Value as string
        field_name: Name of the field for error messages

    Returns:
        Validated positive integer

    Raises:
        ValueError: If value is invalid
    """
    try:
        value = int(value_str)
        if value < 0:
            raise ValueError(f"{field_name} must be positive")
        return value
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"{field_name} must be a number") from e
        raise


def _validate_positive_float(value_str: str, field_name: str) -> float:
    """Validate positive float.

    Args:
        value_str: Value as string
        field_name: Name of the field for error messages

    Returns:
        Validated positive float

    Raises:
        ValueError: If value is invalid
    """
    try:
        value = float(value_str)
        if value < 0:
            raise ValueError(f"{field_name} must be positive")
        return value
    except ValueError as e:
        if "could not convert" in str(e) or "invalid literal" in str(e):
            raise ValueError(f"{field_name} must be a number") from e
        raise


def _validate_not_empty(value_str: str, field_name: str) -> str:
    """Validate not empty.

    Args:
        value_str: Value as string
        field_name: Name of the field for error messages

    Returns:
        Validated not empty string
    """
    if not value_str.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value_str


# ============================================================================
# INPUT HELPERS
# ============================================================================


def _input_with_quit_check(prompt: str, default: Optional[str] = None) -> str:
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


def _input_validated(
    prompt: str,
    validator,
    default: Optional[Any] = None,
    max_attempts: int = 3
):
    """Get input from user with validation.

    Args:
        prompt: The prompt to display
        validator: Function to validate/transform input
        default: Optional default value
        max_attempts: Maximum validation attempts before raising error

    Returns:
        Validated value from validator function

    Raises:
        UserCancelledError: If user enters 'quit' or max attempts exceeded
    """
    for attempt in range(max_attempts):
        try:
            user_input = _input_with_quit_check(prompt, default)
            return validator(user_input)
        except ValueError as e:
            print(f"** Error: {e} **")
            if attempt < max_attempts - 1:
                print(
                    f"Please try again ({max_attempts - attempt - 1} attempts remaining)\n")
            else:
                print("Maximum attempts reached.\n")
                raise UserCancelledError() from e

    # Safety net: if we somehow exit the loop without returning or raising
    raise UserCancelledError("Maximum validation attempts exceeded")


# ============================================================================
# DATA COLLECTION FUNCTIONS
# ============================================================================

def _collect_coin_data(existing_coin: Optional[Coin] = None) -> Dict[str, Any]:
    """Collect coin data from user input.

    Args:
        existing_coin: Optional existing coin for updates (shows as defaults)

    Returns:
        Dictionary containing coin data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    coin = existing_coin if existing_coin else Coin()

    def get_existing_coin_data(attr: str) -> Optional[Any]:
        return getattr(existing_coin, attr, None) if existing_coin else None

    # Collect data with validation
    coin.type_id = _select_coin_type(get_existing_coin_data("type_id"))

    coin.year = _input_validated(
        "Year: ",
        _validate_year,
        get_existing_coin_data("year")
    )

    coin.mint_mark = _input_with_quit_check(
        "Mint Mark: ", get_existing_coin_data("mint_mark") or DEFAULT_MINT_MARK
    )

    coin.condition_id = _select_condition(
        get_existing_coin_data("condition_id"))

    coin.quantity = _input_validated(
        "Quantity: ",
        lambda x: _validate_positive_int(x, "Quantity"),
        get_existing_coin_data("quantity")
    )

    coin.value_estimate = _input_validated(
        "Value Estimate: ",
        lambda x: _validate_positive_float(x, "Value Estimate"),
        get_existing_coin_data("value_estimate")
    )

    coin.acquired_from = _input_with_quit_check(
        "Acquired From: ", get_existing_coin_data("acquired_from")
    )

    coin.notes = _input_with_quit_check(
        "Notes: ", get_existing_coin_data("notes")
    )

    return coin.to_dict()


def _collect_coin_type_data(
    existing_coin_type: Optional[CoinType] = None
) -> Dict[str, Any]:
    """Collect coin type data from user input.

    Args:
        existing_coin_type: Optional existing coin type for updates

    Returns:
        Dictionary containing coin type data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    coin_type = existing_coin_type if existing_coin_type else CoinType()

    def get_existing_coin_type_data(attr: str) -> Optional[Any]:
        return getattr(existing_coin_type, attr, None) if existing_coin_type else None

    coin_type.name = _input_with_quit_check(
        "Enter new coin type name: ", get_existing_coin_type_data("name")
    )

    coin_type.denomination = _input_with_quit_check(
        "Enter coin type denomination: (e.g. 1 Dollar, 1 Cent) ",
        get_existing_coin_type_data("denomination")
    )

    coin_type.country_id = _select_country(
        get_existing_coin_type_data("country_id")
    )

    coin_type.metal = _input_with_quit_check(
        "Enter coin type metal: (e.g. Silver, Copper, Nickel) ",
        get_existing_coin_type_data("metal")
    )

    return coin_type.to_dict()


def _collect_condition_data(
    existing_condition: Optional[Condition] = None
) -> Dict[str, Any]:
    """Collect condition data from user input.

    Args:
        existing_condition: Optional existing condition for updates

    Returns:
        Dictionary containing condition data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    condition = existing_condition if existing_condition else Condition()

    def get_existing_condition_data(attr: str) -> Optional[Any]:
        return getattr(existing_condition, attr, None) if existing_condition else None

    condition.name = _input_with_quit_check(
        "Enter new condition name using the Shelldon Scale (e.g. MS-65): ",
        get_existing_condition_data("name")
    )

    condition.description = _input_with_quit_check(
        "Enter condition description: (e.g. Mint State 65, Very Fine 20) ",
        get_existing_condition_data("description")
    )

    return condition.to_dict()


def _collect_country_data(
    existing_country: Optional[Country] = None
) -> Dict[str, Any]:
    """Collect country data from user input.

    Args:
        existing_country: Optional existing country for updates

    Returns:
        Dictionary containing country data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    country = existing_country if existing_country else Country()

    def get_existing_country_data(attr: str) -> Optional[Any]:
        return getattr(existing_country, attr, None) if existing_country else None

    country.name = _input_with_quit_check(
        "Enter new country name: ", get_existing_country_data("name")
    )

    country.country_code = _input_with_quit_check(
        "Enter new country code: ", get_existing_country_data("country_code")
    )

    return country.to_dict()


# ============================================================================
# SELECTION FUNCTIONS
# ============================================================================

def _select_coin_type(selected_coin_type_id: Optional[int] = None) -> int:
    """Allow user to select a coin type or add a new one.

    Args:
        selected_coin_type_id: Optional current coin type ID (for updates)

    Returns:
        Selected or newly created coin type ID

    Raises:
        UserCancelledError: If user cancels the operation
    """
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
                "Select coin type: ", default_position
            )
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
                print(MSG_INVALID_CHOICE)
        except ValueError:
            print("Please enter a valid number.")

    return coin_type_id


def _select_condition(selected_condition_id: Optional[int] = None) -> int:
    """Allow user to select a condition or add a new one.

    Args:
        selected_condition_id: Optional current condition ID (for updates)

    Returns:
        Selected or newly created condition ID

    Raises:
        UserCancelledError: If user cancels the operation
    """
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
                "Select condition: ", default_position
            )
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
                print(MSG_INVALID_CHOICE)
        except ValueError:
            print("Please enter a valid number.")

    return condition_id


def _select_country(selected_country_id: Optional[int] = None) -> Optional[int]:
    """Allow user to select a country by entering country code.

    Args:
        selected_country_id: Optional current country ID (for updates)

    Returns:
        Country ID matching the entered country code

    Raises:
        UserCancelledError: If user cancels the operation
    """
    countries = get_countries()
    default_country_code = None

    if selected_country_id:
        for country in countries:
            if country['id'] == selected_country_id:
                default_country_code = country['country_code']
                break

    while True:
        try:
            country_code = _input_validated(
                "Enter coin type country code: (e.g. CA, US, etc...) ",
                lambda x: _validate_not_empty(x, "Country Code"),
                default_country_code
            )
            break
        except ValueError:
            print("Please enter a valid country code.")
    return get_country_id_by_code(country_code)


# ============================================================================
# PUBLIC API FUNCTIONS
# ============================================================================

def get_coin_input() -> Dict[str, Any]:
    """Get coin input from the user.

    Returns:
        Dictionary containing coin data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    return _collect_coin_data()


def get_coin_type_input() -> Dict[str, Any]:
    """Get coin type input from the user.

    Returns:
        Dictionary containing coin type data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    return _collect_coin_type_data()


def get_condition_input() -> Dict[str, Any]:
    """Get condition input from the user.

    Returns:
        Dictionary containing condition data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    return _collect_condition_data()


def get_country_input() -> Dict[str, Any]:
    """Get country input from the user.

    Returns:
        Dictionary containing country data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    return _collect_country_data()


def get_updated_coin_input(coin_id: str) -> Dict[str, Any]:
    """Get updated coin input from the user with current values as defaults.

    Args:
        coin_id: ID of the coin to update

    Returns:
        Dictionary containing updated coin data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    selected_coin = get_coin_by_id(coin_id)
    coin = Coin(**selected_coin)

    print("\n** Press Enter to keep current value, or type new value **\n")

    return _collect_coin_data(coin)


def get_updated_coin_type_input(coin_type_id: str) -> Dict[str, Any]:
    """Get updated coin type input from the user with current values as defaults.

    Args:
        coin_type_id: ID of the coin type to update

    Returns:
        Dictionary containing updated coin type data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    selected_coin_type = get_coin_type_by_id(coin_type_id)
    coin_type = CoinType(**selected_coin_type)

    return _collect_coin_type_data(coin_type)


def get_updated_condition_input(condition_id: str) -> Dict[str, Any]:
    """Get updated condition input from the user with current values as defaults.

    Args:
        condition_id: ID of the condition to update

    Returns:
        Dictionary containing updated condition data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    selected_condition = get_condition_by_id(condition_id)
    condition = Condition(**selected_condition)

    return _collect_condition_data(condition)


def get_updated_country_input(country_id: str) -> Dict[str, Any]:
    """Get updated country input from the user with current values as defaults.

    Args:
        country_id: ID of the country to update

    Returns:
        Dictionary containing updated country data

    Raises:
        UserCancelledError: If user cancels the operation
    """
    selected_country = get_country_by_id(country_id)
    country = Country(**selected_country)

    return _collect_country_data(country)


# ============================================================================
# CONFIRMATION FUNCTIONS
# ============================================================================

def confirm_delete_coin_input(coin: Dict[str, Any]) -> str:
    """Get confirm delete coin input from the user.

    Args:
        coin: Dictionary containing coin data to display

    Returns:
        'DELETE' if user confirmed deletion

    Raises:
        UserCancelledError: If user enters 'quit' or refuses to confirm
    """
    print("\n** Type 'DELETE' to delete the following coin, or 'QUIT' to cancel: **\n")
    print(f"Coin ID: {coin['id']}")
    print(f"Coin Type: {coin['coin_type_name']}")
    print(f"Coin Year: {coin['year']}")
    print(f"Coin Mint Mark: {coin['mint_mark']}")
    print(f"Coin Condition: {coin['condition_name']}")
    print(f"Coin Quantity: {coin['quantity']}")
    print(f"Coin Value Estimate: {coin['value_estimate']}")
    print(f"Coin Acquired From: {coin['acquired_from']}\n")

    while True:
        confirmation = _input_with_quit_check("Confirm delete coin: ")
        if confirmation.upper() == CONFIRM_DELETE_TEXT:
            return CONFIRM_DELETE_TEXT
        else:
            print(
                f"** Invalid input. Type '{CONFIRM_DELETE_TEXT}' to confirm or 'QUIT' to cancel. **\n")


def confirm_delete_coin_type_input(coin_type: Dict[str, Any]) -> str:
    """Get confirm delete coin type input from the user.

    Args:
        coin_type: Dictionary containing coin type data to display

    Returns:
        'DELETE' if user confirmed deletion

    Raises:
        UserCancelledError: If user enters 'quit' or refuses to confirm
    """

    print("\n** Type 'DELETE' to delete the following coin type, or 'QUIT' to cancel: **\n")
    print(f"Coin Type ID: {coin_type['id']}")
    print(f"Coin Type Name: {coin_type['name']}")
    print(f"Coin Type Denomination: {coin_type['denomination']}")
    print(f"Coin Type Country: {coin_type['country_name']}")
    print(f"Coin Type Metal: {coin_type['metal']}\n")

    while True:
        confirmation = _input_with_quit_check("Confirm delete coin type: ")
        if confirmation.upper() == CONFIRM_DELETE_TEXT:
            return CONFIRM_DELETE_TEXT
        else:
            print(
                f"** Invalid input. Type '{CONFIRM_DELETE_TEXT}' to confirm or 'QUIT' to cancel. **\n")


def confirm_delete_condition_input(condition: Dict[str, Any]) -> str:
    """Get confirm delete condition input from the user.

    Args:
        condition: Dictionary containing condition data to display

    Returns:
        'DELETE' if user confirmed deletion

    Raises:
        UserCancelledError: If user enters 'quit' or refuses to confirm
    """
    print("\n** Type 'DELETE' to delete the following condition, or 'QUIT' to cancel: **\n")
    print(f"Condition ID: {condition['id']}")
    print(f"Condition Name: {condition['name']}")
    print(f"Condition Description: {condition['description']}\n")

    while True:
        confirmation = _input_with_quit_check("Confirm delete condition: ")
        if confirmation.upper() == CONFIRM_DELETE_TEXT:
            return CONFIRM_DELETE_TEXT
        else:
            print(
                f"** Invalid input. Type '{CONFIRM_DELETE_TEXT}' to confirm or 'QUIT' to cancel. **\n")


def confirm_delete_country_input(country: Dict[str, Any]) -> str:
    """Get confirm delete country input from the user.

    Args:
        country: Dictionary containing country data to display

    Returns:
        'DELETE' if user confirmed deletion

    Raises:
        UserCancelledError: If user enters 'quit' or refuses to confirm
    """
    print("\n** Type 'DELETE' to delete the following country, or 'QUIT' to cancel: **\n")
    print(f"Country ID: {country['id']}")
    print(f"Country Name: {country['name']}")
    print(f"Country Code: {country['country_code']}\n")

    while True:
        confirmation = _input_with_quit_check("Confirm delete country: ")
        if confirmation.upper() == CONFIRM_DELETE_TEXT:
            return CONFIRM_DELETE_TEXT
        else:
            print(
                f"** Invalid input. Type '{CONFIRM_DELETE_TEXT}' to confirm or 'QUIT' to cancel. **\n")
