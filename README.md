# csv-formatter-rs

## General info

This Python script transforms CSV data feeds for Rentsense into the correct format.
It uses the Pandas library to read the data and do the following:

* Removes whitespaces and other characters which could cause issues when processing.
* Checks for required data feed headers, adds in if not there.
* Parses any date field into YYYY/MM/DD format.
* Check each row of data to make sure there is complete data.
* Adds in default values for certain columns if null.


## Pre-Requisites/Setup

To run this project, install Pandas & detect_delimiter using pip.
```
pip install Pandas
pip instal detect_delimiter
```
* Script will look for the name of the file, rent_actions must be renamed to rent.actions*
* Make sure all file names are spelt correctly, eg: ‘tenants’ not ‘tennants’

## Usage

Place the script within the directory of all the raw CSV files you would like to cleanse.
Then run the following command in a new CMD prompt within the directory:
```
python csv-formatter-rs.py
```
You will be presented with the following menu: 

```
        Please enter number of which feed(s) you want to transform:
        1. rent.accounts
        2. rent.transactions
        3. rent.actions
        4. rent.arrangements
        5. rent.balances
        6. rent.tenants
        7. rent.contacts
        8. rent.hmsrecommendations
        9. Transform all rent files
```
The menu will appear asking which feed you want to clean.

Always try 9 for all files, if there an issue with a file it script will stop running there and you will have to manually rerun for each file using the menu.

Once the script has run succesfully, it will create a folder in the directory called "Cleaned Files" and ouput CSV's will be named correctly for Rentsense. 

# Common Errors

* Rentsense requires each word to be capitalised for e.g. AccountReference even though is spelt together both main letters need to be capitalised, accountreference will not work in RentSense*.

* Columns Expected = x, Actual Columns = y, Line number = Z
	This is due to an extra delimiter in the raw files. Edit the file in notepad++ and remove the extra delimiter. And type Y to Run the file. 
  
 Note: Do not open cleaned files in excel and save as the date format will be changed. Use notepad++ for editing



