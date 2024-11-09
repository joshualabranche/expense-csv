#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 15:11:53 2024

@author: jlab
"""

import csv
import sys


def get_int_input():
    raw = ''
    while raw.isdigit() == False:
        raw = input('enter expense account id number (0 for help): ')
    return int(raw) 

filename = sys.argv[1]

expenses = ['Costs of Good Sold',
            'Advertising and Marketing',
            'Automobile Expense',
            'Bank Fees and Charges',
            '[ INSURANCE ] Liability Insurance',
            'Other Expenses',
            'Printing and Stationary',
            'Rent Expense',
            'Repairs and Maitenance',
            'Tax Paid Expense',
            'Office Supplies',
            'Square Fees',
            'Stripe Fees',
            'Licensing and Permits']

month_expenses = []
with open(filename + '.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        month_expenses.append(row)
        
csvwrite = open(filename + '-zoho.csv', 'w', newline='')
spamwriter = csv.writer(csvwrite, delimiter=' ')
spamwriter.writerow(['Entry Number','Expense Date','Expense Account','Paid Through','Expense Amount','Expense Description'])

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
                1  - 'Costs of Good Sold'
                2  - 'Advertising and Marketing'
                3  - 'Automobile Expense'
                4  - 'Bank Fees and Charges'
                5  - '[ INSURANCE ] Liability Insurance'
                6  - 'Other Expenses'
                7  - 'Printing and Stationary'
                8  - 'Rent Expense'
                9  - 'Repairs and Maitenance'
                10 - 'Tax Paid Expense'
                11 - 'Office Supplies'
                12 - 'Square Fees'
                13 - 'Stripe Fees'
                14 - 'Licensing and Permits'
                  """)
            print(f'Current expense from: {vendor} for: $' + '{:0.2f}'.format(amount))
            raw = get_int_input() 
        else:
            print("""\n*** enter a valid expense account id or '0' for help ***""")
            print(f'Current expense from: {vendor} for: $' + '{:0.2f}'.format(amount))
            raw = get_int_input() 
    account = expenses[raw-1]
    
    # write the data to the csv file
    spamwriter.writerow([curr,date,account,paid_through,amount,descript])
    
csvwrite.close()