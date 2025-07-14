from CartManager import CartManager


def main():
    cart = CartManager()

    # Adding items
    cart.add_item("Apple", 0.99, 3)
    cart.add_item("Banana", 1.49)
    cart.add_item("Apple", 0.99, 2)  # Should merge quantities

    # Display cart
    print("\nCart Contents:")
    for item in cart.get_all_items():
        print(f"- {item}")

    # Update quantity
    cart.update_quantity("Banana", 5)

    # Remove item
    cart.remove_item("Apple")

    # Final state
    print("\nFinal Cart:")
    for item in cart.get_all_items():
        print(f"- {item}")
    print(f"Subtotal: ${cart.subtotal():.2f}")
    print(f"Total Items: {cart.total_items()}")


if __name__ == "__main__":
    main()