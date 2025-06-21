from inventory import Inventory


def main():
    inv = Inventory()
    while True:
        cmd = input("Enter command [a=add, r=remove, q=quit]: ").strip().lower()
        if cmd == 'q':
            break
        barcode = input("Barcode: ").strip()
        try:
            qty = int(input("Quantity: "))
        except ValueError:
            print("Please enter a valid integer quantity.")
            continue
        try:
            if cmd == 'a':
                inv.add(barcode, qty)
                print(f"Added {qty} of {barcode}.")
            elif cmd == 'r':
                inv.remove(barcode, qty)
                print(f"Removed {qty} of {barcode}.")
            else:
                print("Unknown command.")
                continue
        except ValueError as e:
            print("Error:", e)
            continue
        print("Current stock:", inv.all_items())


if __name__ == "__main__":
    main()
