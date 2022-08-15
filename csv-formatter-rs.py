import pandas as pd
from datetime import datetime
import csv
import time
import sys
import os
from detect_delimiter import detect

def main():
    user_menu()

def user_menu():
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

def auto_detected_delimiter():
    ''' Function used to determine the delimiter set 
        Automatically, defaults to comma but will 
        detect other seperators if ! comma.
        Returns delimiter, can feed into any function'''
    with open('rent.accounts20220808.csv', newline='') as csvfile:
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

def auto_detected_file(file_contains, delimiter):
    for file_counter in os.listdir('.'):
        if file_contains.lower() in file_counter.lower():
            file = file_counter
    if file == '':
        print('*********************************************************************************************************************************************************')
        sys.exit('Cant find file that contains ' + file_contains + ', please rename file accordingly, program will now exit.')
        print('*********************************************************************************************************************************************************')
    else:
        print('File found: ' + file)
    return file

def initialise_dataframe(file, delimiter):
    df = pd.read_csv(file, skipinitialspace = True, encoding ='utf-8', encoding_errors = 'backslashreplace', converters = {'accountreference' : lambda x: str(x)}, sep = delimiter, keep_default_na=False)
    return df

def account_validation(file, df):
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
    badColumns = 0
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        firstRow = next(reader)
        columnLength = len(firstRow)
        for row in reader:
            if len(row) == 0:
                continue
            elif len(row) < columnLength:
                print ('Columns Expected = ' + str(columnLength) + ', Actual Columns = ' + str(len(row)) + '. Line number: ' + str(reader.line_num))
                badColumns =+1
            elif len(row) > columnLength:
                print ('Columns Expected = ' + str(columnLength) + ', Actual Columns = ' + str(len(row)) + '. Line number: ' + str(reader.line_num))
                badColumns =+1
    csvfile.close()
    if (badColumns >= 1):
        print('*********************************************************************************************************************************************************')
        playerChoice = input('Check the files output and fix those before you proceed with cleanse, You can override this by pressing y or Y or press anything to exit and review file.')
        print('*********************************************************************************************************************************************************')
        if playerChoice.lower() != 'y':
            print('*************************')
            sys.exit('Program now terminated')
            print('*************************')

def getdelimiterValueWithValidation():
    ''' NOT IN USE ANYMORE'''
    delimiterVal = '' 
    while True:
        delimiterVal = input('Please enter a delimiter value of | or , or tab: ')
        if delimiterVal not in ('|', ',', 'tab'):
            print("Not an appropriate choice.")
        elif (delimiterVal == 'tab'):
            delimiterVal = '\t'
            break
        else:
            break
    return delimiterVal        

def transform_dataframe(file, df):
    #load CSV as panda dataframe - converters keeps padding in accountReference
    print(df.head(10))
    print(df.dtypes)
    #delete all commas in the dataframe and replace with null
    df.replace(',','', regex = True, inplace = True)
    print ('Replaced all commas with null value.')
    #delete all commas in the dataframe and replace with null
    df.replace("'",'', regex = True, inplace = True)
    print ('Replaced all apostrophes with null value.')
    df.replace('NULL','', regex = True, inplace = True)
    df.replace('null','', regex = True, inplace = True)
    print ('Replaced the word null with empty value.')

def date_parser(file, df):
    #Timestamp('2262-04-11 23:47:16.854775807') limitation for year
    # search for all columns with date then only parse them
    if 'acc' in file.lower():
        account_validation(file, df)
        df['TenancyStartDate'] = pd.to_datetime(df.TenancyStartDate, dayfirst=True)
        print('Parsed TenancyStartDate into date value.')
        #convert date into DD-MM-YYYY format for Rentsense
        df['TenancyStartDate'] = df['TenancyStartDate'].dt.strftime('%Y-%m-%d')
         # Force AccountReference column as string
        df.astype({'AccountReference':'string'})
        df['AccountReference'] = df['AccountReference'].astype(str).str.strip()
        print('TenancyStartDate converted to YYYY-MM-DD.')
    elif 'tra' in file.lower():
        df['TransactionPostDate'] = pd.to_datetime(df.TransactionPostDate, dayfirst=True)
        df['TransactionDate'] = pd.to_datetime(df.TransactionDate, dayfirst=True)
        print('Parsed Transaction dates into date value.')
        #convert date into DD-MM-YYYY format for Rentsense
        df['TransactionPostDate'] = df['TransactionPostDate'].dt.strftime('%Y-%m-%d')
        df['TransactionDate'] = df['TransactionDate'].dt.strftime('%Y-%m-%d')
        df['AccountReference'] = df['AccountReference'].astype(str).str.strip()
        print('Transaction dates converted to YYYY-MM-DD.')
        # Deletes trailing white space on column.
        df['TransactionSign'] = df['TransactionSign'].str.strip()
        df['TransactionDescription'] = df['TransactionDescription'].str.strip()
    elif 'rent.action' in file.lower():
        df['ActionDate'] = pd.to_datetime(df.ActionDate, dayfirst=True)
        print('Parsed ActionDate into date value.')
        #convert date into YYYY-MM-DD format for Rentsense
        df['ActionDate'] = df['ActionDate'].dt.strftime('%Y-%m-%d')
        df['AccountReference'] = df['AccountReference'].astype(str).str.strip()
        print('ActionDate converted to YYYY-MM-DD.')       
    elif 'arr' in file.lower():   
        df['AgreementStartDate'] = pd.to_datetime(df.AgreementStartDate, dayfirst=True)
        df['AgreementEndDate'] = pd.to_datetime(df.AgreementEndDate, dayfirst=True)
        print('Parsed AgreementStartDate into date value.')
        print('Parsed AgreementEndDate into date value.')
        #convert date into YYYY-MM-DD format for Rentsense
        df['AgreementStartDate'] = df['AgreementStartDate'].dt.strftime('%Y-%m-%d')
        df['AgreementEndDate'] = df['AgreementEndDate'].dt.strftime('%Y-%m-%d')
        df['AccountReference'] = df['AccountReference'].astype(str).str.strip()              
        print('AgreementStartDate converted to YYYY-MM-DD.')
        print('AgreementEndDate converted to YYYY-MM-DD.')  
    elif 'bal' in file.lower():   
        df['BalanceDate'] = pd.to_datetime(df.BalanceDate, dayfirst=True)
        print('Parsed BalanceDate into date value.')
        #convert date into YYYY-MM-DD format for Rentsense
        df['BalanceDate'] = df['BalanceDate'].dt.strftime('%Y-%m-%d')
        df['AccountReference'] = df['AccountReference'].astype(str).str.strip()              
        print('BalanceDate converted to YYYY-MM-DD.')      
    elif 'cont' in file.lower():   
        df['ContactDate'] = pd.to_datetime(df.ContactDate, dayfirst=True)
        print('Parsed ContactDate into date value.')
        #convert date into YYYY-MM-DD format for Rentsense
        df['ContactDate'] = df['ContactDate'].dt.strftime('%Y-%m-%d')
        df['AccountReference'] = df['AccountReference'].astype(str).str.strip()              
        print('ContactDate converted to YYYY-MM-DD.')
    elif 'rec' in file.lower():   
        df['RecommendedActionDate'] = pd.to_datetime(df.RecommendedActionDate, dayfirst=True)
        #df['RecommendedActionDate'] = pd.to_datetime(df.RecommendedActionDate, format = '%d-%b')
        print('Parsed RecommendedActionDate into date value.')
        #convert date into YYYY-MM-DD format for Rentsense
        df['RecommendedActionDate'] = df['RecommendedActionDate'].dt.strftime('%Y-%m-%d')
        df['AccountReference'] = df['AccountReference'].astype(str).str.strip()              
        print('RecommendedActionDate converted to YYYY-MM-DD.')
    else:
        print('Did not parse any dates, check file name for issues.')

def get_current_date():
    date = datetime.date(datetime.now())
    date = date.strftime('%Y%m%d')
    return date

def write_to_csv(filename, df):
    df.astype(str)
    print ('forced all columns as string.')
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
    df.replace('nan','', regex = True, inplace = True)
    df.to_csv(filename + str(get_current_date()) + '.csv', encoding ='utf-8', index = False)
    print(str(time.process_time()) + ' seconds taken to clean feed.')
    os.chdir(existingPath)

def controller(file_contains, filename_write):
    delimiter = auto_detected_delimiter()
    file = auto_detected_file(file_contains, delimiter)
    check_row_length(delimiter, file)
    df = initialise_dataframe(file, delimiter)
    transform_dataframe(file, df)
    date_parser(file, df)
    write_to_csv(filename_write, df)

if __name__ == "__main__":
    main()
