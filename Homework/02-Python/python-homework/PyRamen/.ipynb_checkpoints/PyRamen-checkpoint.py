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
    menu_reader = csv.reader(menu_csv, delimiter = ".")
    mheader = next(menu_reader)
    for mrow in menu_reader:
        menu.append(mrow)

# Read in the sales data into the sales list
with open (sales_filepath,'r') as sales_csv:
    sales_reader = csv.reader(sales_csv, delimiter = ".")
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
    line_item_id = sales_row[0] 
    date = sales_row[1]
    cc_number = sales_row[2] 
    qty = sales_row[3]
    menu_item = sales_row[4]

    # If the item value not in the report, add it as a new entry with initialized metrics
    # Naming convention allows the keys to be ordered in logical fashion, count, revenue, cost, profit
    if !(report.haskey(menu_item)):
        
        report[menu_item] = {"01-count":0,
                            "02-revenue":0,
                            "03-cogs":0,
                            "04-profit":0}

    # @TODO: For every row in our sales data, loop over the menu records to determine a match
    for menu_row

        # Item,Category,Description,Price,Cost
        # @TODO: Initialize menu data variables




        # @TODO: Calculate profit of each item in the menu data


        # @TODO: If the item value in our sales data is equal to the any of the items in the menu, then begin tracking metrics for that item


            # @TODO: Print out matching menu data






            # @TODO: Cumulatively add up the metrics for each item key





        # @TODO: Else, the sales item does not equal any fo the item in the menu data, therefore no match



    # @TODO: Increment the row counter by 1


# @TODO: Print total number of records in sales data




# @TODO: Write out report to a text file (won't appear on the command line output)
