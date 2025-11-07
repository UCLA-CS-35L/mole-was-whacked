"""A faulty vending machine."""

import csv
import argparse
from dataclasses import dataclass
from typing import List, Optional, Tuple
from algo import edit_distance, coin_change, subset_sum

# flake8: noqa

@dataclass
class Item:
    """Represents a snack in the vending machine."""
    name: str
    price: int


def load_machine(file_path: str) -> List[List[Optional[Item]]]:
    """Load CSV into a row-major 2D grid (rows outer, columns inner)."""
    machine: List[List[Optional[Item]]] = []

    with open(file_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            r = int(row["row"]) - 1
            c = ord(row["column"].upper()) - ord("A")

            # ensure enough rows
            while len(machine) <= r:
                machine.append([])

            # ensure row has enough columns
            while len(machine[r]) <= c:
                machine[r].append(None)

            machine[r][c] = Item(name=row["name"], price=int(row["price"]))

    return machine


def print_machine(machine: List[List[Optional[Item]]]) -> None:
    """Print the vending machine grid with columns A,B,C and rows 1,2,3."""
    if not machine:
        print("Vending machine is empty.")
        return

    max_cols = max(len(row) for row in machine)

    # column headers
    print("    ", end="")
    for c in range(max_cols):
        print(f"{chr(ord('A') + c):^8}", end="")
    print("\n" + "   " + "-" * (max_cols * 8))

    # print each row
    for r_idx, row in enumerate(machine, start=1):
        print(f"{r_idx:<3}| ", end="")
        for c_idx in range(max_cols):
            item = row[c_idx] if c_idx < len(row) else None
            if item:
                print(f"{item.name[:7]:^8}", end="")
            else:
                print(f"{'???':^8}", end="")
        print()


def find_snack(machine: List[List[Optional[Item]]], query: str
              ) -> Optional[Tuple[int,int]]:
    """Return coordinates of snack closest to query using edit distance."""
    best_dist = float("inf")
    best_pos: Optional[Tuple[int,int]] = None
    best_item: Optional[Item] = None

    for r_idx, row in enumerate(machine):
        for c_idx, item in enumerate(row):
            if not item:
                continue
            dist = edit_distance(item.name.lower(), query.lower())
            if dist < best_dist:
                best_dist = dist
                best_pos = (c_idx, r_idx)
                best_item = item

    if best_item and best_item.name != query:
        print(f"Did you mean '{best_item.name}'?")
    return best_pos


def get_price(machine: List[List[Optional[Item]]], query: str) -> Optional[int]:
    """Return price of snack found via fuzzy search."""
    pos = find_snack(machine, query)
    if pos is None:
        return None
    r, c = pos
    return machine[r][c].price


def buy_item(machine: List[List[Optional[Item]]], cell: str, money: int) -> None:
    """Purchase an item by cell coordinate and print change."""
    col_letter = cell[0].upper()
    row_number = int(cell[1:])

    r = row_number - 1
    c = ord(col_letter) - ord("A")

    if c >= len(machine) or r >= len(machine[c]) or not machine[c][r]:
        print("Invalid selection")
        return

    item = machine[c][r]

    if money < item.price:
        print(f"Insufficient money. {item.name} costs ${item.price}, "
              f"you provided ${money}")
        return

    change = coin_change([100, 50, 25, 10, 5, 1], money - item.price)
    print(f"Purchased {item.name} for ${item.price}. Change: {change}")


def exact_combination(machine: List[List[Optional[Item]]], amount: int) -> None:
    """Check if any subset of items sums exactly to amount."""
    all_prices = [item.price for row in machine for item in row if item]
    if subset_sum(all_prices, amount):
        print(f"A combination of items sums exactly to ${amount}")
    else:
        print(f"No combination sums exactly to ${amount}")


def main() -> None:
    """CLI entry point for vending machine."""
    parser = argparse.ArgumentParser(description="Vending Machine CLI")
    parser.add_argument("file", help="CSV file with vending machine data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("print", help="Print vending machine layout")

    parser_price = subparsers.add_parser("price", help="Get price of a snack")
    parser_price.add_argument("snack", help="Name of snack")

    parser_buy = subparsers.add_parser("buy", help="Buy an item by cell")
    parser_buy.add_argument("cell", help="Cell coordinate (e.g., A3)")
    parser_buy.add_argument("money", type=int, help="Amount of money provided")

    parser_exact = subparsers.add_parser(
        "exact", help="Check subset sum for exact budget"
    )
    parser_exact.add_argument("amount", type=int, help="Target amount to spend")

    args = parser.parse_args()
    machine = load_machine(args.file)

    if args.command == "print":
        print_machine(machine)
    elif args.command == "price":
        price = get_price(machine, args.snack)
        if price is None:
            print(f"{args.snack} not found")
        else:
            print(f"Price of {args.snack} is ${price}")
    elif args.command == "buy":
        buy_item(machine, args.cell, args.money)
    elif args.command == "exact":
        exact_combination(machine, args.amount)


if __name__ == "__main__":
    main()
