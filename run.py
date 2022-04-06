import pprint
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures from the user.
    """
    while True:
        print('Please enter sales data from the last market.')
        print('The data should be writen as six numbers seperated by commas.')
        print('Example: 10, 20, 30, 40, 50, 60\n')

        data_str = input('Enter your data here: ')

        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data is valid!')
            break
    
    return sales_data

def validate_data(values):
    
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True



def calculate_surplus_data(sales_row):
    """
    Compare ammount of sold sanwitches with stock and calculate surplus for each sandwich type

    The surplus is defined as the sales figures subtracted from the stock
    -A negative number indicates extra made when item sold out
    -A positive number indicates waste
    """
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(data, worksheet):
    """
    Takes ints and updates the correct worksheet with the provided data
    """
    print(f"updating the {worksheet} worksheet...")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet succesfully updated\n")

def get_last_five_entries_sales():
    """
    Collects data from worksheet, collects the last five entries for each sandwitch and returns the data as a list of lists
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to love sandwitches data Automation!\n")
#main()

sales_columns = get_last_five_entries_sales()

    