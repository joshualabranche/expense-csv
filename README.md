# expense-csv

need to make spreadsheets from TD statements first
 - copy and paste only expense content as is

add checks, bank fees, and withdrawals
 - manually added in
 - four rows
    - date: "MM/DD needs the  ", MM is the month, and DD is the year
    - description 1: "check number x", "bank", or "ATM"
    - description 2: describe what for (fees, licnesing, etc)
    - amount: dollar amount

run the script in the terminal with the newly created expense sheet
$ python3 expense-makecsv.py "new_expense_sheet.csv"

program will prompt user to ennter expense account id for every expense

output will be "new_expense_csv-zoho.csv"

save as .xlsx file and upload to zoho books 
