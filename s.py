import requests
import pandas as pd

# Replace 'your_alpha_vantage_api_key' with your actual API key from Alpha Vantage
API_KEY = 'your_alpha_vantage_api_key'
BASE_URL = 'https://www.alphavantage.co/query'

# Function to get real-time stock data
def get_stock_price(symbol):
    try:
        url = f"{BASE_URL}?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        if 'Global Quote' in data:
            return {
                'symbol': symbol,
                'price': float(data['Global Quote']['05. price']),
            }
        else:
            print(f"No data found for symbol: {symbol}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return None

class Portfolio:
    def _init_(self):
        self.stocks = {}

    def add_stock(self, symbol, quantity):
        stock_data = get_stock_price(symbol)
        if stock_data:
            if symbol in self.stocks:
                self.stocks[symbol] += quantity
            else:
                self.stocks[symbol] = quantity
            print(f"Added {quantity} of {symbol} to your portfolio.")
        else:
            print(f"Cannot add {symbol} to your portfolio as it is not a valid symbol.")

    def remove_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] -= quantity
            if self.stocks[symbol] <= 0:
                del self.stocks[symbol]
            print(f"Removed {quantity} of {symbol} from your portfolio.")
        else:
            print(f"Cannot remove {symbol} as it is not in your portfolio.")

    def get_portfolio_value(self):
        total_value = 0
        for symbol, quantity in self.stocks.items():
            stock_data = get_stock_price(symbol)
            if stock_data:
                total_value += stock_data['price'] * quantity
        return total_value

    def display_portfolio(self):
        portfolio_data = []
        for symbol, quantity in self.stocks.items():
            stock_data = get_stock_price(symbol)
            if stock_data:
                stock_value = stock_data['price'] * quantity
                portfolio_data.append([symbol, quantity, stock_data['price'], stock_value])
            else:
                portfolio_data.append([symbol, quantity, 'N/A', 'N/A'])
        df = pd.DataFrame(portfolio_data, columns=['Symbol', 'Quantity', 'Price', 'Total Value'])
        print(df)
        print(f"Total Portfolio Value: ${self.get_portfolio_value():.2f}")

# Main function to interact with the user
def main():
    portfolio = Portfolio()

    while True:
        print("\nPortfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            try:
                quantity = int(input("Enter quantity: "))
                portfolio.add_stock(symbol, quantity)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            try:
                quantity = int(input("Enter quantity: "))
                portfolio.remove_stock(symbol, quantity)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        elif choice == '3':
            portfolio.display_portfolio()
        elif choice == '4':
            print("Exiting Portfolio Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    main()