#!/usr/bin/env python
# Gwydion Oostvogel, Jelle Westerbos, Sophie Schubert


import sys
from helpers.load_data import create_grid


def main():
    # Check for correct number of arguments.
    if len(sys.argv) != 2:
        print("Usage: Python Application.py <1, 2 or 3>")
        sys.exit(1)
    version = sys.argv[1]

    # Create grid
    grid = create_grid(0, 50, 50, version)
    # Check
    print(grid)


if __name__ == "__main__":
    main()
