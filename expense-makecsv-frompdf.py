#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:30:02 2025

@author: jlab
"""

import csv
import pypdf
import tkinter as tk
from tkinter import filedialog

def get_expense_lines(page, month, expense_start, expense_end, first_page=False, last_page=False):
    month_to_int = {
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
        }
    days = []
    for i in range(31):
        days.append(str(i+1).zfill(2))
    line_numbers = []
    line_num = 0
    if not last_page:
        for line in page:
            if any([(str(month_to_int[month]).zfill(2) + '/' + x) == line[0:5] for x in days]):
                if first_page:
                    if line_num >= expense_start:
                        line_numbers.append(line_num)
                else:
                    line_numbers.append(line_num)
            line_num += 1
    else:
        for line in page:
            if line=='Other Withdrawals':
                break
            else:
                if any([(str(month_to_int[month]).zfill(2) + '/' + x) == line[0:5] for x in days]):
                # if line[0:2] == str(month_to_int[month]):
                    line_numbers.append(line_num)
                line_num += 1
    return line_numbers

def get_file_path():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()

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

def main():
    # pull file name from command line
    filepath = get_file_path()
    filename = filepath.split('/')[-1]
    outname  = '/' + '/'.join(filepath.split('/')[1:-1]) + '/expense' + filename[-15:-4]
    
    # load up the pdf statement
    pdf_file = pypdf.PdfReader(filepath)
    num_pages = pdf_file.get_num_pages()
    
    # what year is it?
    #year = datetime.datetime.now().strftime("%Y")[2::]
    year = pdf_file.pages[0].extract_text().splitlines()
    month = year[7][-11:-8]
    year  = year[7][-2::]
    
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
            if (page_lines[10] == 'Electronic Payments (continued)') or (page_lines[0] == 'How to Balance your Account'):
                expense_page_end += 1
        else:
            break
    
    # look for the last payment line on the page where electronic payments end
    expense_line_end = 0
    page_lines = pdf_file.pages[expense_page_end].extract_text().splitlines()
    for lines in page_lines:
        if lines[0:9]=='Subtotal:':
            if (expense_line_end < expense_line_start) and (expense_page_start==expense_page_end):
                expense_line_end += 1
            else:
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
        # get the lines that are the start of an expense
        expense_lines = get_expense_lines(page_lines,month,expense_line_start,expense_line_end,page_num==expense_page_start,page_num==expense_page_end)
        # get any lines of expenses that are only 1 line long
        line_diff = []
        for i in range(len(expense_lines)-1):
            line_diff.append(expense_lines[i+1]-expense_lines[i])
        expense_one_liners = [i for i,x in enumerate(line_diff) if x==1]
        expense_one_liners = [expense_lines[x] for x in expense_one_liners]
       
        # process unique case where there is only one page
        if expense_page_start == expense_page_end:

            for expense_line in expense_lines:
                if any([x==expense_line for x in expense_one_liners]):
                    # handle one liners here
                    continue
                else:
                    date = page_lines[expense_line].split(' ')[0] + '/' + year
                    descript = '_'.join(page_lines[expense_line].split(' ')[1::])
                    vendor = page_lines[expense_line+1]
                    card = page_lines[expense_line+2]
                    amount = float(page_lines[expense_line+3])
                paid_through = 'Sauwce LLC'
                
                # prompt user to assign epense to an account
                raw = get_expense_account(expenses, vendor, amount)
        
                # expense account id is defined by given user index for expenses list
                account = expenses[raw-1]
        
                # write the data to the csv file
                spamwriter.writerow([expense_num,date,account,paid_through,amount,vendor])
                expense_num += 1
            break
        # process the first page here as it may start at any line
        if page_num == expense_page_start:
            for expense_line in expense_lines:
                if any([x==expense_line for x in expense_one_liners]):
                    # handle one liners here
                    continue
                else:
                    date = page_lines[expense_line].split(' ')[0] + '/' + year
                    descript = '_'.join(page_lines[expense_line].split(' ')[1::])
                    vendor = page_lines[expense_line+1]
                    card = page_lines[expense_line+2]
                    amount = float(page_lines[expense_line+3])
                paid_through = 'Sauwce LLC'
                
                # prompt user to assign epense to an account
                raw = get_expense_account(expenses, vendor, amount)
        
                # expense account id is defined by given user index for expenses list
                account = expenses[raw-1]
        
                # write the data to the csv file
                spamwriter.writerow([expense_num,date,account,paid_through,amount,vendor])
                expense_num += 1
        # process the last page here as it may end on any line
        elif page_num == expense_page_end:

            for expense_line in expense_lines:
                if any([x==expense_line for x in expense_one_liners]):
                    # handle one liners here
                    continue
                else:
                    date = page_lines[expense_line].split(' ')[0] + '/' + year
                    descript = '_'.join(page_lines[expense_line].split(' ')[1::])
                    vendor = page_lines[expense_line + 1]
                    card = page_lines[expense_line + 2]
                    amount = float(page_lines[expense_line + 3])
                paid_through = 'Sauwce LLC'
                
                # prompt user to assign epense to an account
                raw = get_expense_account(expenses, vendor, amount)
        
                # expense account id is defined by given user index for expenses list
                account = expenses[raw-1]
        
                # write the data to the csv file
                spamwriter.writerow([expense_num,date,account,paid_through,amount,vendor])
                expense_num += 1
        # process the middle pages
        else:
            #skip the "How to Balance Page"
            if page_lines[0]=="How to Balance your Account":
                continue
    

            for expense_line in expense_lines:
                if any([x==expense_line for x in expense_one_liners]):
                    # handle one liners here
                    continue
                else:
                    date = page_lines[expense_line].split(' ')[0] + '/' + year
                    descript = '_'.join(page_lines[expense_line].split(' ')[1::])
                    vendor = page_lines[expense_line + 1]
                    card = page_lines[expense_line + 2]
                    amount = float(page_lines[expense_line + 3])
                paid_through = 'Sauwce LLC'
                
                # prompt user to assign epense to an account
                raw = get_expense_account(expenses, vendor, amount)
        
                # expense account id is defined by given user index for expenses list
                account = expenses[raw-1]
        
                # write the data to the csv file
                spamwriter.writerow([expense_num,date,account,paid_through,amount,vendor])
                expense_num += 1
    
    # close csv file
    csvwrite.close()
    

if __name__ == "__main__":
    main()