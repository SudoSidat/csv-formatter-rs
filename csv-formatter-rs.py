import pandas as pd
from datetime import datetime
import csv
import time
import sys
import os
from detect_delimiter import detect
import inspect


def main():
    user_menu()

def user_menu():
    ''' Looped menu to provide different options for user.
        Single file transformation or all files transformation.'''
    while True:
        menuInput = input("""
        Please enter number of which feed you want to clean:
        1. rent.accounts
        2. rent.transactions
        3. rent.actions
        4. rent.arrangements
        5. rent.balances
        6. rent.tenants
        7. rent.contacts
        8. rent.hmsrecommendations
        9. All files.
        """)

        if menuInput.isdigit() == False:
            print("Not an appropriate choice, please enter a number.")
        else:
            menuInput = int(menuInput)
            break
            
    if menuInput == 1:
        controller('acc', 'rent.accounts')
    elif menuInput == 2:
        controller('trans', 'rent.transactions')
    elif menuInput == 3:
        controller('rent.action', 'rent.actions')
    elif menuInput == 4:
        controller('arrang', 'rent.arrangements')   
    elif menuInput == 5:
        controller('balan', 'rent.balances')          
    elif menuInput == 6:
        controller('tenan', 'rent.tenants')          
    elif menuInput == 7:
        controller('conta', 'rent.contacts')                  
    elif menuInput == 8:
        controller('rec', 'rent.hmsrecommendations')                  
    elif menuInput == 9:
        controller('acc', 'rent.accounts')
        controller('trans', 'rent.transactions')
        controller('rent.action', 'rent.actions')
        controller('arrang', 'rent.arrangements')   
        controller('balan', 'rent.balances')          
        controller('tenan', 'rent.tenants')          
        controller('conta', 'rent.contacts')                  
        controller('rec', 'rent.hmsrecommendations')                            
    else:
        sys.exit(0)

def auto_detected_delimiter(file):
    ''' Function used to determine the delimiter set 
        Automatically, defaults to comma but will 
        detect other seperators if ! comma.
        Returns delimiter, can feed into any function'''
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        row1 = next(reader)  # gets the first line
        csvfile.close()
        delimiter = detect(row1[0])
        if delimiter == None: 
            delimiter = ','
            print ('Delimiter = ' + delimiter)
        else: 
            print ('Delimiter = ' + delimiter)
    return delimiter

def auto_detected_file(file_contains):
    ''' Uses str.contains to search for prefix
        of file names, if not found, program will
        terminate.'''
    for file in os.listdir('.'):
        if file_contains.lower() in file.lower():
            print('Found a file match')
            break
        else:
            file = ''

    if file == '':
        sys.exit('Cant find file that contains ' + file_contains + ', please rename file accordingly, program will now exit.')
    else:
        print('File found: ' + file)
    return file

def initialise_dataframe(file, delimiter):
    ''' Creates Panadas dataframe from csv read data.'''
    df = pd.read_csv(file, skipinitialspace = True, encoding ='utf-8', encoding_errors = 'backslashreplace', converters = {'accountreference' : lambda x: str(x)}, sep = delimiter, keep_default_na=False)
    return df

def account_validation(file, df):
    ''' Validation specific to rent.accounts, checks for value
        in LocalAuthority field if null then it will fill default data.'''
    if ('acc' in file.lower()):
        df.loc[(df.LocalAuthority == '') | (df.LocalAuthority == 'Unknown') | (df.LocalAuthority == 'NULL'), 'LocalAuthority'] = "Default HB Cycle"
        print('******************************************************************************************************************************')
        print('A Cycle called "Default HB Cycle" was added in as there were blank tenancies found, check this in LocalAuthority Field.')
        print('******************************************************************************************************************************')
        # try catch added if NeedsCategory doesn't exist it will create the column with a default value
        try:
            df.loc[(df.NeedsCategory == ''|""|" "),'NeedsCategory'] = "Default Data"
        except: 
            df['NeedsCategory'] = ''
            df.loc[(df.NeedsCategory == ''),'NeedsCategory'] = "Default Data"
            print('NeedsCategory column has now been added with default value')

def check_row_length(delimiter, file):
    ''' Finds the number of columns 
        Compares number to the no. of Rows
        Flags if there's a mismatch.
        Can Continue program or terminate if issues found.'''
    bad_columns = 0
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        first_row = next(reader)
        column_length = len(first_row)
        for row in reader:
            if len(row) == 0:
                continue
            elif len(row) < column_length:
                print ('Columns Expected = ' + str(column_length) + ', Actual Columns = ' + str(len(row)) + '. Line number: ' + str(reader.line_num))
                bad_columns =+1
            elif len(row) > column_length:
                print ('Columns Expected = ' + str(column_length) + ', Actual Columns = ' + str(len(row)) + '. Line number: ' + str(reader.line_num))
                bad_columns =+1
    csvfile.close()
    if (bad_columns >= 1):
        print('*********************************************************************************************************************************************************')
        menu_choice = input('Check the files output and fix those before you proceed with cleanse, You can override this by pressing y or Y or press anything to exit and review file.')
        print('*********************************************************************************************************************************************************')
        if menu_choice.lower() != 'y':
            print('*************************')
            sys.exit('Program now terminated')
            print('*************************')

def transform_dataframe(file, df):
    ''' Takes out commas, nulls, apostrophe values
        from the data.'''
    #load CSV as panda dataframe - converters keeps padding in accountReference
    print(df.head(10))
    #delete all commas in the dataframe and replace with null
    df.replace(',','', regex = True, inplace = True)
    print ('Replaced all commas with null value.')
    #delete all commas in the dataframe and replace with null
    df.replace("'",'', regex = True, inplace = True)
    print ('Replaced all apostrophes with null value.')
    df.replace('NULL','', regex = True, inplace = True)
    df.replace('null','', regex = True, inplace = True)
    print ('Replaced the word null with empty value.')

def date_parserv2(df):
    #Timestamp('2262-04-11 23:47:16.854775807') limitation for year in Pandas library
    ''' Finds all columns with 'date' within them.
        Gathers them into a list and parses into
        date format YYYY-MM-DD'''
    date_columns = []
    column_headers = list(df.columns.values)
    for column in column_headers:
        if 'date' in column.lower():
            date_columns.append(column)
        else:
            next
    if len(date_columns) > 0:
        print ('List of date fields to_parse: ' + str(date_columns))
        for to_parse in date_columns:
            #Convert date into DD-MM-YYYY format for Rentsense
            print('Parsed ' + to_parse + ' into date value.')          
            df[to_parse] = pd.to_datetime(df[to_parse], dayfirst=True)
            df[to_parse] = df[to_parse].dt.strftime('%Y-%m-%d')
    else:
        print('No date columns to parse.')

def get_current_date():
    ''' Used for writing into the filename.'''
    date = datetime.date(datetime.now())
    date = date.strftime('%Y%m%d')
    return date

def write_to_csv(filename, df):

    existingPath = os.getcwd()
    newPath = os.getcwd() + '\Cleaned Files'
    try:
        os.mkdir(newPath)
    except OSError:
        print ("Successfully saved in directory: %s " % newPath)
    else:
        print ("Successfully created the directory %s " % newPath)
    os.chdir(newPath)
    #takes out null occurences after parsing dataframe as string
    df.astype(str)
    df.replace('nan','', regex = True, inplace = True)
    df.to_csv(filename + str(get_current_date()) + '.csv', encoding ='utf-8', index = False)
    print(str(time.process_time()) + ' seconds taken to clean feed.')
    os.chdir(existingPath)

def controller(file_contains, filename_write):
    file = auto_detected_file(file_contains)
    delimiter = auto_detected_delimiter(file)
    check_row_length(delimiter, file)
    df = initialise_dataframe(file, delimiter)
    transform_dataframe(file, df)
    date_parserv2(df)
    write_to_csv(filename_write, df)

if __name__ == "__main__":
    main()
