# Scrape-Linkedin
Python script that scrapes of all the Careem employees in Pakistan.

This code uses Selenium and BeautifulSoup to extract information about Careem Employees in Pakistan. The information include name, title, location, profile. 
The output data is stored in a csv file, i.e., output_search.csv.

The intodb.py file loads the output_search.csv file into pandas dataframe. It cleans the data like removes extra whitespaces, capitalize each first letter of each word in the name.
It stores the information in a sqlite database. The database name is employees_details.db, and the table name is careem_employees. 
The exported data from the database is stored in careem_employees.csv file.

