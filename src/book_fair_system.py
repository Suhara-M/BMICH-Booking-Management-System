# --- 1. DATA STRUCTURES ---

# DICTIONARY: Store User Accounts for fast lookup
user_accounts = {"admin": "1234"}

# TREE: Categorized Item Catalogue
catalogue_tree = {
    "Books": {
        "B001": {"item": "Mill on the Floss", "price": 3000.00},
        "B002": {"item": "Macbeth", "price": 4000.00},
        "B003": {"item": "Madolduwa", "price": 2000.00}
    },
    "Stationery": {
        "S001": {"item": "Single Writing Book (120 pages book)", "price": 300.00},
        "S002": {"item": "Ink pen", "price": 250.00},
        "S003": {"item": "A4 bundle", "price": 400.00}
    }
}

# STACK: Conceptual Order ID Generation (Popping ensures uniqueness)
order_id_stack = [f"ORD-{i:04d}" for i in range(1000, 2000)]
# Push onto stack in reverse order to preserve ascending popping
order_id_stack.reverse()

# QUEUE: Manage customers waiting for checkout
customer_queue = collections.deque(["Customer_1"])


# LINKED LIST: Order History Management
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class OrderHistory:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node


history_log = OrderHistory()
total_revenue = 0.0


# --- 2. LOGIC FUNCTIONS ---

def login_process():
    """
    STRICT IMPLEMENTATION OF FLOWCHART 1
    """
    print("\n--- Welcome to Colombo Book Fair Site ---")

    # Step: Do you have an account?
    has_account = input("Do you have an account? (yes/no): ").lower().strip()

    if has_account == "no":
        # Step: Create New Account
        new_user = input("Create Username: ").strip()
        new_pass = input("Create Password: ").strip()
        user_accounts[new_user] = new_pass
        # Step: Account Created
        print(">> Account Created Successfully.")

    # Step: Enter the Login Details (Repeats if Login Successful? is No)
    while True:
        print("\n--- Please Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Decision: Login Successful?
        if username in user_accounts and user_accounts[username] == password:
            print(">> Login Successful!")
            return True  # Path: Yes -> Go to Shopping
        else:
            print(">> Login Failed! Invalid username or password.")  # Path: No -> Loop back



def shopping_process():
    cart = {}
    undo_stack = []  # Stores item codes in order added

    print("\n--- Displaying Catalogue ---")
    for category, items in catalogue_tree.items():
        print(f"\n[{category}]")
        for code, details in items.items():
            print(f"  {code}: {details['item']} - LKR {details['price']}")

    while True:
        action = input("\nEnter Code to add, 'undo' to remove last added item, or 'done' to checkout: ").lower().strip()
        if action == 'done':
            return cart, undo_stack
        elif action == 'undo':
            if undo_stack:
                last_code = undo_stack.pop()
                if last_code in cart:
                    print(f">> Undone: Removed all of {cart[last_code]['name']} from cart")
                    del cart[last_code]
                    if not cart:
                        print(">> Cart is now empty.")
                else:
                    print(">> Error: Item not found in cart.")
            else:
                print(">> Nothing to undo.")
            continue

        # Add item to cart
        found = False
        for category in catalogue_tree.values():
            if action.upper() in category:
                item_code = action.upper()
                try:
                    qty = int(input(f"Enter quantity for {category[item_code]['item']}: "))
                    if qty <= 0:
                        raise ValueError
                except ValueError:
                    print("Invalid quantity.")
                    found = True
                    break

                cart[item_code] = {"name": category[item_code]['item'],
                                   "price": category[item_code]['price'],
                                   "qty": qty}

                # Push the item code only once, not per quantity
                undo_stack.append(item_code)
                print(">> Item added to Cart.")
                found = True
                break

        if not found:
            print(">> Error: Invalid Item Code.")
def checkout_process(cart,undo_stack):
#Calculation, review cart, and record keeping
    global total_revenue
    if not cart:
        print(">> Cart is empty. Cannot proceed to checkout.")
        return False

    # --- REVIEW CART LOOP ---
    while True:
        print("\n--- Reviewing Cart ---")
        total_amount = 0
        for code, info in cart.items():
            subtotal = info['price'] * info['qty']
            total_amount += subtotal
            print(f" {info['name']} (x{info['qty']}) = LKR {subtotal}")
# Proceed to checkout
        print(f"Subtotal: LKR {total_amount}")
        confirm = input("Confirm to Checkout? (yes/no): ").lower().strip()

        if confirm == 'yes':
            break  # exit the loop and continue to payment
        elif confirm == 'no':
            # Allow customer to undo items if needed
            if undo_stack:
                undo_input = input("Do you want to remove the last added item? (yes/no): ").lower().strip()
                if undo_input == 'yes':
                    last_code = undo_stack.pop()
                    if last_code in cart:
                        print(f">> Removed all of {cart[last_code]['name']} from cart")
                        del cart[last_code]
                        if not cart:
                            print(">> Cart is now empty. Checkout cancelled.")
                            return False
                else:
                    print(">> Continuing cart review...")
            else:
                print(">> Nothing to undo. Continuing cart review...")
        else:
            print(">> Invalid input. Please type 'yes' or 'no'.")

    # --- Payment ---
    order_id = order_id_stack.pop()
    print(f">> Order ID Generated: {order_id}")
    print("\nPAYMENT OPTIONS:")
    print("1. Online Payment (3% processing fee)")
    print("2. On-site Payment (no additional charges)")

    pay_method = input("Payment Method (online/on-site): ").lower().strip()
    final_price = total_amount
    if pay_method == "online":
        final_price *= 1.03
        print(f"Net Total (with 3% fee): LKR {final_price}")
        input("Enter Payment Details: ")
        print(">> Payment Successful!")
    else:
        print(">> Please pay on-site at the book fair.")

    # Save to history
    history_log.append({
        "ID": order_id,
        "Cart": cart.copy(),
        "Payment": pay_method,
        "Amount": final_price
    })
    total_revenue += final_price
    display_bill(order_id, final_price, pay_method)
    return True

def display_bill(order_id, total, payment_method):
    print("\n--- BILL ---")
    print(f"Order ID: {order_id}")
    print(f"Payment Method: {payment_method}")
    print(f"Total Amount: LKR {total}")


def search_order():
    order_id = input("Enter Order ID to search: ").strip()

    current = history_log.head
    while current:
        if current.data["ID"] == order_id:
            print("\n--- ORDER FOUND ---")
            print(f"Order ID: {current.data['ID']}")
            print(f"Payment Method: {current.data['Payment']}")
            print("Items:")
            for code, info in current.data["Cart"].items():
                print(f"  {info['name']} (x{info['qty']})")
            print(f"Total Amount: LKR {current.data['Amount']}")
            return
        current = current.next

    print(">> Order not found.")


# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    while customer_queue:
        current_customer = customer_queue.popleft()
        print(f"\n--- Processing {current_customer} ---")

        if login_process():  # Step: Go to Shopping
            user_cart, undo_stack = shopping_process()

            if user_cart:  # Cart has items
                checkout_process(user_cart, undo_stack)
            else:  # Cart is empty
                print(">> You didn't add any items to the cart.")

        # Step: Is there more customers?
        more = input("\nIs there another customer? (yes/no): ").lower()
        if more == 'yes':
            customer_queue.append(f"Customer_{len(user_accounts) + 1}")

    # Step: Display the final total revenue
    print(f"\n" + "=" * 40)
    print(f"FINAL TOTAL REVENUE: LKR {total_revenue}")
    print("=" * 40)
    print("End of Business Day.")
