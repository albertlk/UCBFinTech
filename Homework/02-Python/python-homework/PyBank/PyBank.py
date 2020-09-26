# Importing necessary libraries
from pathlib import Path
import csv

# Writing file path for budget_data.csv
csv_path = Path("Resources/budget_data.csv")

# Creating list of dictionaries for P&L data
pnl_data = []

# Reading in data from csv file
with open (csv_path,'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ",")
    header = next(csv_reader)
    # print(header)
    # Saving data in pnl dictionary
    for row in csv_reader:
        # print(row)
        pnl_data.append({header[0]:row[0], header[1]:int(row[1])}) 

# Initializing variables
months = 0
net_total = 0
change = 0
large_inc = 0
large_inc_date = ""
large_dec = 0
large_dec_date = ""
prev_pnl = 0

# Iterating through pnl_data to find above metrics
for entry in pnl_data:
    # This month's data
    pnl = entry["Profit/Losses"]
    date = entry["Date"]
    delta = pnl - prev_pnl
    
    # Calculating the change in profit and loss
    if months == 0:
        change = 0
    else:
        change += delta

    # Checking to see if it is the largest increase or largest decrease
    if delta > large_inc:
        large_inc = delta
        large_inc_date = date
    elif delta < large_dec:
        large_dec = delta
        large_dec_date = date
    
    # Incrementing variables
    months += 1
    net_total += pnl
    prev_pnl = pnl

# Defining output path
csv_out = Path("PnL_Summary.txt")

# Writing to txt and printing to terminal
with open (csv_out, 'a') as file:
    print("Financial Analysis")
    file.write("Financial Analysis\n")
    
    print("-"*30)
    file.write("-"*30)
    file.write("\n")
    
    print(f"Total Months: {months}")
    file.write(f"Total Months: {months}\n")
    
    print(f"Total: ${net_total}")
    file.write(f"Total: ${net_total}\n")
    
    avg_change = round(change/(months-1),2)
    print(f"Average Change: ${avg_change}")
    file.write(f"Average Change: ${avg_change}\n")
    
    print(f"Greatest Increase in Profits: {large_inc_date} ${large_inc}")
    file.write(f"Greatest Increase in Profits: {large_inc_date} ${large_inc}\n")
    
    print(f"Greatest Decrease in Profits: {large_dec_date} ${large_dec}")
    file.write(f"Greatest Decrease in Profits: {large_dec_date} ${large_dec}\n")