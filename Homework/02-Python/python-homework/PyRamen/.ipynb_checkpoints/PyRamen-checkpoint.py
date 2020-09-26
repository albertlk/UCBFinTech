# Import libraries
import csv
from pathlib import Path

# Set file paths for menu_data.csv and sales_data.csv
menu_filepath = Path('Resources/menu_data.csv')
sales_filepath = Path('Resources/sales_data.csv')

# Initialize list objects to hold our menu and sales data
menu = []
sales = []

# Read in the menu data into the menu list
with open (menu_filepath,'r') as menu_csv:
    menu_reader = csv.reader(menu_csv, delimiter = ",")
    mheader = next(menu_reader)
    for mrow in menu_reader:
        menu.append(mrow)

# Read in the sales data into the sales list
with open (sales_filepath,'r') as sales_csv:
    sales_reader = csv.reader(sales_csv, delimiter = ",")
    sheader = next(sales_reader)
    for srow in sales_reader:
        sales.append(srow)

# Initialize dict object to hold our key-value pairs of items and metrics
report = {}

# Initialize a row counter variable
row_count = 0

# Loop over every row in the sales list object
for sales_row in sales:

    # Line_Item_ID,Date,Credit_Card_Number,Quantity,Menu_Item
    # Initialize sales data variables
    qty = int(sales_row[3])
    menu_item = sales_row[4]

    # If the item value not in the report, add it as a new entry with initialized metrics
    # Naming convention allows the keys to be ordered in logical fashion, count, revenue, cost, profit
    if menu_item not in report:
        
        report[menu_item] = {"01-count":0,
                            "02-revenue":0,
                            "03-cogs":0,
                            "04-profit":0}

    #For every row in our sales data, loop over the menu records to determine a match
    for menu_row in menu:
        
        # Item,Category,Description,Price,Cost
        item = menu_row[0]
        price = float(menu_row[3])
        cost = float(menu_row[4])

        # Calculate profit of each item in the menu data
        profit = price - cost
        
        # If the item value in our sales data is equal to the any of the items in the menu, then begin tracking metrics for that item
        if menu_item == item:

            # Print out matching menu data
            print(f"{menu_item} matches {item} on the menu!")

            # Cumulatively add up the metrics for each item key
            report[menu_item]["01-count"] += qty
            report[menu_item]["02-revenue"] += price * qty
            report[menu_item]["03-cogs"] += cost * qty
            report[menu_item]["04-profit"] += profit * qty
            
            # Breaking from menu loop once a match has been found
            break

        # Else, the sales item does not equal any of the item in the menu data, therefore no match
        else:
            print(f"{menu_item} does not equal {item}! No Match!")

    # Increment the row counter by 1
    row_count += 1

# Print total number of records in sales data
print(f"The total number of records in sales data is: {row_count}")

# Write out report to a text file (won't appear on the command line output)
# Set file paths for output file
report_filepath = Path('report.txt')

with open (report_filepath, 'a') as file:
    for report_row in report:
        file.write(f"{report_row} {report[report_row]}\n")