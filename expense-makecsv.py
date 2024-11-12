#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 15:11:53 2024

@author: jlab
"""

import csv
import sys

# define function to prompt user input that checks for valid inputs
def get_int_input():
    raw = ''
    while raw.isdigit() == False:
        raw = input('enter expense account id number (0 for help): ')
    return int(raw) 

# pull file name from command line
filename = sys.argv[1]

# expense account id list
expenses = ['Cost of Goods Sold',
            'Advertising and Marketing',
            'Automobile Expense',
            'Bank Fees and Charges',
            'Liability Insurance',
            'Other Expenses',
            'Printing and Stationary',
            'Rent Expense',
            'Repairs and Maintenance',
            'Tax Paid Expense',
            'Office Supplies',
            'Square Fees',
            'Stripe Fees',
            'Licensing and Permits',
            'Telephone Expense',
            'Furniture and Equipment',
            'Meals and Entertainment']

# using the given csv file, load the data into month expenses
month_expenses = []
with open(filename + '.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in csvreader:
        month_expenses.append(row)
        
# modify the data and save the reformatted data to a new file 'filename-zoho.csv'
csvwrite = open(filename + '-zoho.csv', 'w', newline='')
csvwriter = csv.writer(csvwrite, delimiter=' ')

# write header info
csvwriter.writerow(['Entry Number','Expense Date','Expense Account','Paid Through','Expense Amount','Expense Description'])

# loop through data in csv file and reorganize for parsing in zoho
for curr in range(int(len(month_expenses)/4)):
    date = month_expenses[curr*4][0][1::] + '/24'
    paid_through = 'Sauwce LLC'
    amount = float(month_expenses[curr*4+3][0])
    descript = '_'.join(month_expenses[curr*4+0][1::]) + '_' + '_'.join(month_expenses[curr*4+1])
    vendor = '_'.join(month_expenses[curr*4+1])
    
    # prompt user to assign expense account id to expense
    print(f'Current expense from: {vendor} for: $' + '{:0.2f}'.format(amount))
    raw = get_int_input()   
    while not 0 < raw < len(expenses) + 1:
        if raw == 0:
            print("""
                0  - HELP
                1  - 'Cost of Goods Sold'
                2  - 'Advertising and Marketing'
                3  - 'Automobile Expense'
                4  - 'Bank Fees and Charges'
                5  - 'Liability Insurance'
                6  - 'Other Expenses'
                7  - 'Printing and Stationary'
                8  - 'Rent Expense'
                9  - 'Repairs and Maintenance'
                10 - 'Tax Paid Expense'
                11 - 'Office Supplies'
                12 - 'Square Fees'
                13 - 'Stripe Fees'
                14 - 'Licensing and Permits'
                15 - 'Telephone Expense'
                16 - 'Furniture and Equipment'
                17 - 'Meals and Entertainment'
                  """)
            print(f'Current expense from: {vendor} for: $' + '{:0.2f}'.format(amount))
            raw = get_int_input() 
        else:
            print("""\n*** enter a valid expense account id or '0' for help ***""")
            print(f'Current expense from: {vendor} for: $' + '{:0.2f}'.format(amount))
            raw = get_int_input() 
    # expense account id is defined by given user index for expenses list
    account = expenses[raw-1]
    
    # write the data to the csv file
    csvwriter.writerow([curr,date,account,paid_through,amount,descript])

# close csv file
csvwrite.close()
