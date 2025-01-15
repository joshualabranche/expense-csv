#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:30:02 2025

@author: jlab
"""

import csv
import pypdf
import sys

# define function to prompt user input that checks for valid inputs
def get_int_input():
    raw = ''
    while raw.isdigit() == False:
        raw = input('enter expense account id number (0 for help): ')
    return int(raw) 

# define function to clean up user input expense account
def get_expense_account(expenses,vendor,amount):
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
                16 - 'Fruniture and Equipment'
                  """)
            print(f'Current expense from: {vendor} for: $' + '{:0.2f}'.format(amount))
            raw = get_int_input() 
        else:
            print("""\n*** enter a valid expense account id or '0' for help ***""")
            print(f'Current expense from: {vendor} for: $' + '{:0.2f}'.format(amount))
            raw = get_int_input()          
    return raw

# pull file name from command line
filename = sys.argv[1]
outname  = sys.argv[2]

# load up the pdf statement
pdf_file = pypdf.PdfReader(filename)
num_pages = pdf_file.get_num_pages()

# look for the page and line where electronic payments start
expense_page_start = 0
expense_line_start = 0
found_page = False
for current_page in range(num_pages):
    page_lines = pdf_file.pages[current_page].extract_text().splitlines()
    for lines in page_lines:
        if lines=='Electronic Payments':
            found_page = True
            break
        expense_line_start += 1
    if found_page==True:
        break
    else:
        expense_line_start = 0
    expense_page_start += 1
expense_line_start += 2

# look for the page where electronic payments end
expense_page_end = expense_page_start
found_page = False
for current_page in range(expense_page_start+1,num_pages):
    page_lines = pdf_file.pages[current_page].extract_text().splitlines()
    if len(page_lines) > 10:
        if page_lines[10] == 'Electronic Payments (continued)':
            expense_page_end += 1
    else:
        break

# look for the last payment line on the page where electronic payments end
expense_line_end = 0
page_lines = pdf_file.pages[expense_page_end].extract_text().splitlines()
for lines in page_lines:
    if lines[0:9]=='Subtotal:':
        break
    else:
        expense_line_end += 1

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
            'Furniture and Equipment']
        
# modify the data and save the reformatted data to a new file 'filename-zoho.csv'
csvwrite = open(outname + '-zoho.csv', 'w', newline='')
spamwriter = csv.writer(csvwrite, delimiter=' ')

# write header info
spamwriter.writerow(['Entry Number','Expense Date','Expense Account','Paid Through','Expense Amount','Expense Description'])

# counter to keep track of the expense number
expense_num = 0
for page_num in range(expense_page_start,expense_page_end+1):
    # pull the lines from the current page
    page_lines = pdf_file.pages[page_num].extract_text().splitlines()
    # process unique case where there is only one page
    if expense_page_start == expense_page_end:
        num_expenses = int((expense_line_end - expense_line_start)/4)
        for curr in range(num_expenses):
            date = page_lines[expense_line_start+4*0].split(' ')[0] + '/24'
            descript = '_'.join(page_lines[expense_line_start+4*0].split(' ')[1::])
            vendor = page_lines[expense_line_start+1+4*curr]
            card = page_lines[expense_line_start+2+4*curr]
            amount = float(page_lines[expense_line_start+3+4*curr])
            paid_through = 'Sauwce LLC'
            
            # prompt user to assign epense to an account
            raw = get_expense_account(expenses, vendor, amount)
    
            # expense account id is defined by given user index for expenses list
            account = expenses[raw-1]
    
            # write the data to the csv file
            spamwriter.writerow([expense_num,date,account,paid_through,amount,descript])
            expense_num += 1
        break
    # process the first page here as it may start at any line
    if page_num == expense_page_start:
        num_expenses = int((len(page_lines) - expense_line_start)/4)
        for curr in range(num_expenses):
            date = page_lines[expense_line_start+4*0].split(' ')[0] + '/24'
            descript = '_'.join(page_lines[expense_line_start+4*0].split(' ')[1::])
            vendor = page_lines[expense_line_start+1+4*curr]
            card = page_lines[expense_line_start+2+4*curr]
            amount = float(page_lines[expense_line_start+3+4*curr])
            paid_through = 'Sauwce LLC'
            
            # prompt user to assign epense to an account
            raw = get_expense_account(expenses, vendor, amount)
    
            # expense account id is defined by given user index for expenses list
            account = expenses[raw-1]
    
            # write the data to the csv file
            spamwriter.writerow([expense_num,date,account,paid_through,amount,descript])
            expense_num += 1
    # process the last page here as it may end on any line
    elif page_num == expense_page_end:
        num_expenses = int((expense_line_end-12)/4)
        for curr in range(num_expenses):
            date = page_lines[12+4*0].split(' ')[0] + '/24'
            descript = '_'.join(page_lines[12+4*0].split(' ')[1::])
            vendor = page_lines[13+4*curr]
            card = page_lines[14+4*curr]
            amount = float(page_lines[15+4*curr])
            paid_through = 'Sauwce LLC'
            
            # prompt user to assign epense to an account
            raw = get_expense_account(expenses, vendor, amount)
    
            # expense account id is defined by given user index for expenses list
            account = expenses[raw-1]
    
            # write the data to the csv file
            spamwriter.writerow([expense_num,date,account,paid_through,amount,descript])
            expense_num += 1
    # process the middle pages
    else:
        for curr in range(int((len(page_lines)-12)/4)):
            date = page_lines[12+4*0].split(' ')[0] + '/24'
            descript = '_'.join(page_lines[12+4*0].split(' ')[1::])
            vendor = page_lines[13+4*curr]
            card = page_lines[14+4*curr]
            amount = float(page_lines[15+4*curr])
            paid_through = 'Sauwce LLC'
            
            # prompt user to assign epense to an account
            raw = get_expense_account(expenses, vendor, amount)
    
            # expense account id is defined by given user index for expenses list
            account = expenses[raw-1]
    
            # write the data to the csv file
            spamwriter.writerow([expense_num,date,account,paid_through,amount,descript])
            expense_num += 1

# close csv file
csvwrite.close()
