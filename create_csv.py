#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:29:42 2026

@author: jlab
"""

import csv

def create_csv_file(file_name):
  """Creates a CSV file based on user-defined inputs, allowing string data."""

  data = []
  column_names = ['Item', 'Description','yes','no']
  try:
      with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line[0]=='#':
                data.append([line.split('# ')[1]])
            elif line!='\n':
                data.append([line.split('\n')[0],' ','-','-'])

        filename = file_name.split('.')[0]
        with open(filename+'.csv', 'w', newline='') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(column_names)
          writer.writerows(data)

        print(f"CSV file '{filename}' created successfully.")
  except Exception as e:
        print(f"An error occurred: {e}")

  return data

if __name__ == "__main__":
    file_name = input('Filename: ')
    create_csv_file(file_name)