"""Main module for the Coin Tracker Database."""

import sys
from pages import main_page

if __name__ == "__main__":
    try:
        main_page()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
