from http.client import OK
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
    ''' Looped menu to provide different options for user.
        Single file transformation or all files transformation.'''
    while True:
        menuInput = input("""
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
        controller('tena', 'rent.tenants')          
    elif menuInput == 7:
        controller('cont', 'rent.contacts')                  
    elif menuInput == 8:
        controller('rec', 'rent.hmsrecommendations')                  
    elif menuInput == 9:
       controller_all_files()     
    else:
        sys.exit(0)

def auto_detected_delimiter(file):
    ''' Function used to determine the delimiter set 
        Automatically, defaults to comma but will 
        detect other seperators if ! comma.
        Returns delimiter, can feed into any function'''
    with open(file, newline = '') as csvfile:
        firstline = csvfile.readline()
        delimiter = detect(firstline) 
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
            break
        else:
            file = ''
    if file == '':
        print('---------------------------------------------------------------------------------------------------------------"')
        sys.exit('Cant find file that contains ' + file_contains + ', please rename file accordingly, program will now exit.')
        print('---------------------------------------------------------------------------------------------------------------"')
    else:
        print('---------------------------------------------------"')
        print('File found: ' + file)
        print('---------------------------------------------------"')
    return file

def auto_detected_all_files():
    ''' Function runs when user selects to transform all files. str.contains to search for prefix
        of file names, if not found, program will terminate, else returns a list of feeds found,
        used in controller_all_files.
    '''
    rent_account = 'acc'
    rent_actions = 'rent.action'
    rent_arrangements = 'arrang'
    rent_balances = 'balan'
    rent_contacts = 'cont'
    rent_hmsrecommendations = 'rec'
    rent_tenants = 'tena'
    rent_transactions = 'trans'

    feeds = {}
    check_file_contains = [rent_account,rent_actions,rent_arrangements,rent_balances,rent_contacts,
                            rent_hmsrecommendations,rent_tenants,rent_transactions]
    
    for file in os.listdir('.'):
        for file_name_check in check_file_contains:
            if file_name_check in file.lower():
                if file_name_check == rent_account:
                    feeds[file] = 'rent.accounts'
                elif file_name_check == rent_actions:
                    feeds[file] = 'rent.actions'
                elif file_name_check == rent_arrangements:
                    feeds[file] = 'rent.arrangements'      
                elif file_name_check == rent_balances:
                    feeds[file] = 'rent.balances'      
                elif file_name_check == rent_contacts:
                    feeds[file] = 'rent.contacts'               
                elif file_name_check == rent_hmsrecommendations:
                    feeds[file] = 'rent.hmsrecommendations'               
                elif file_name_check == rent_tenants:
                    feeds[file] = 'rent.tenants'               
                elif file_name_check == rent_transactions:
                    feeds[file] = 'rent.transactions'               
            else:
                next
    for f in feeds:
        print ('Feed found: ' + f)
    return feeds

def get_headers(delimiter, file):
    '''Checks first line from file for "Account" If found then headers are valid,
        program will return list of header. if not found then will go through rows,
        until valid row of headers is found. If valid headers found, write to temp CSV,
        temp CSV is renamed to original file deleting invalid data and only keeping
        valid headers. If headers not found, program is terminated with error message.
    '''
    list_of_column_names = []
    invalid_header = False
    with open(file, newline = '',encoding='utf-8-sig') as infile:
        reader = csv.reader(infile, delimiter=delimiter)
        row1 = next(reader)
        if(any(item.startswith(("Account", "account")) for item in row1)):
            invalid_header = False
            list_of_column_names = row1
        elif (not list_of_column_names):
            invalid_header = True
            for row in reader:
                if (any(item.startswith(("Account", "account")) for item in row)):
                    invalid_header == False
                    list_of_column_names = row
                    with open('new'+file, 'w', newline='',encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(list_of_column_names)
                        writer.writerows(reader)
                        break
                else: 
                    continue
    if os.path.exists('new'+file):
        os.rename(file,'delete'+file)
        os.rename('new'+file,file)
        os.remove('delete'+file)
    elif not list_of_column_names:
        sys.exit('No valid headers found, check spelling or if headers are in file: ' + file)
    else:
        invalid_header = False

    return list_of_column_names

def check_required_headers(headers_list, file):
    ''' Checks which file is currently being parsed, once identified, the function
        Will get list of headers in file and compare them against the required headers
        for that particular feed. headers_not_found[] list is appended when the header
        required is not found in current file. The list of headers not found is then returned
        so you can add those columns once Dataframe has been initialised.
    '''   
    headers_not_found = []
    headers_to_rename = []
    headers_list = headers_list
    file = file
    rent_account_contains = 'acc'
    rent_actions_contains = 'rent.action'
    rent_arrangements_contains = 'arrang'
    rent_balances_contains = 'balan'
    rent_tenants_contains = 'tena'
    rent_transactions_contains = 'trans'

    check_file_contains = [rent_account_contains,rent_actions_contains,rent_arrangements_contains,
                            rent_balances_contains,rent_tenants_contains,rent_transactions_contains]

    rent_account_required = ["AccountReference","HousingOfficerName",
                            "Patch","TenureType","TenureTypeCode",
                            "TenancyStartDate","LocalAuthority"]
    rent_actions_required = ["AccountReference","ActionCode",
                            "ActionDescription","ActionDate",
                            "ActionSeq"]
    rent_arr_tenants_required = ["AccountReference"]
    rent_arrangements_or = ["ArrangementStartDate", "AgreementStartDate"]          
    rent_arrangements_or2 = ["ArrangementCode", "AgreementCode"]   
    rent_arrangements_or3 = ["ArrangementAmount","AgreementAmount"]       
    rent_balances_required = ["AccountReference","CurrentBalance"]
    rent_transactions_required = ["AccountReference","TransactionDate",
                            "TransactionCode","TransactionAmount"]          
     
    for each_feed in check_file_contains:
        if each_feed.lower() in file.lower():
            file = each_feed
            break
    lower_headers_list = [lower_headers_list.lower() for lower_headers_list in headers_list]
    if file == rent_account_contains:
        for c in rent_account_required:
            if c in headers_list:
                continue
            elif c.lower() in lower_headers_list:
                headers_to_rename.append(c)
            else:
                headers_not_found.append(c)
    elif (file == rent_actions_contains):
        for c in rent_actions_required:
            if c in headers_list:
                continue
            elif c.lower() in lower_headers_list:
                headers_to_rename.append(c)
            else:
                headers_not_found.append(c)      
    elif file == rent_arrangements_contains:
        for c in rent_arr_tenants_required:
            if c in headers_list:
                continue
            elif c.lower() in lower_headers_list:
                headers_to_rename.append(c)
            else:
                headers_not_found.append(c)    
        check_start_date = any(item in rent_arrangements_or for item in headers_list)
        if check_start_date is False:
            headers_not_found.append(rent_arrangements_or[0])
        check_code = any(item in rent_arrangements_or2 for item in headers_list)
        if check_code is False:
            headers_not_found.append(rent_arrangements_or2[0])
        check_amount = any(item in rent_arrangements_or3 for item in headers_list)
        if check_amount is False:
            headers_not_found.append(rent_arrangements_or3[0])
    elif file == rent_balances_contains:
        for c in rent_balances_required:
            if c in headers_list:
                continue
            elif c.lower() in lower_headers_list:
                headers_to_rename.append(c)
            else:
                headers_not_found.append(c) 
    elif file == rent_tenants_contains:
        for c in rent_arr_tenants_required:
            if c in headers_list:
                continue
            elif c.lower() in lower_headers_list:
                headers_to_rename.append(c)
            else:
                headers_not_found.append(c) 
    elif file == rent_transactions_contains:
        for c in rent_transactions_required:
            if c in headers_list:
                continue
            elif c.lower() in lower_headers_list:
                headers_to_rename.append(c)
            else:
                headers_not_found.append(c) 
    if headers_not_found:
        print('------------------------------------------------------------"')
        print('Headers not found: ' + str(headers_not_found))
        print('------------------------------------------------------------"')
    
    return headers_not_found, headers_to_rename


def initialise_dataframe(file, delimiter):
    ''' Creates Pandas dataframe from csv data read, parmeters include removing any non-ascii
        via encoding_errors, converters fill force "AccountReference" into a string to keep it
        intact. Once file is read, assigned to df so we can manipulate the dataframe object.
    '''
    df = pd.read_csv(file, skipinitialspace = True, encoding ='utf-8', encoding_errors = 'backslashreplace', converters = {'AccountReference' : lambda x: str(x)}, sep = delimiter, keep_default_na=False)
    return df

def headers_rename(rename_headers, df):
    ''' Checks the case sensitivity of the headers, Rentsense will not run if case sensitivity
        of headers are wrong, this function will check and correct them. 
    '''
    df = df
    rename_headers = rename_headers
    if not rename_headers:
        print('-----------------------"')
        print('No headers to rename.')
        print('-----------------------"')
    else:
        for h in rename_headers:
            wrong_header = [col for col in df.columns if h.lower() in col.lower()]
            if len(wrong_header) > 0: 
                for column in wrong_header:
                    if column.lower() == h.lower():
                        df.rename(columns = {column:h}, inplace = True)
        if len(wrong_header) > 0:
            print('------------------------------------------------------------"')
            print('Headers to rename: ' + str(wrong_header))
            print('------------------------------------------------------------"')

def add_missing_headers(headers_list, df):
    ''' Takes in list of missing headers, will go through each one adding them in.
        Some headers will need data in them for RentSense to process properly
        If blocks will attempt to add default values into some missing headers.
    '''
    headers_list = headers_list
    for h in headers_list:
        if h == 'LocalAuthority':
            df[h] = ''
            df.loc[(df.LocalAuthority == '') | (df.LocalAuthority == 'Unknown') | (df.LocalAuthority == 'NULL'), 'LocalAuthority'] = "Default HB Cycle"
            print('-------------------------------------------------------------"')
            print('LocalAuthority column now added with "Default HB Cycle".')
            print('Map "Default HB Cycle" in IRR, unless they have multiple LAs.')
            print('If client = Council then map "Default HB Cycle" in IRR as LA.')
            print('-------------------------------------------------------------"')
        elif h == 'Patch':
            df[h] = ''
            df.loc[(df.Patch == ''),'Patch'] = "Default Patch"
            print('-------------------------------------------------------------"')
            print('Patch column has now been added with "Default Patch"')
            print('Advise client to add patch details in next data extract."')
            print('-------------------------------------------------------------"')
        elif h == 'HousingOfficerName':
            df[h] = ''
            df.loc[(df.HousingOfficerName == ''),'HousingOfficerName'] = "Default HousingOfficerName"
            print('-------------------------------------------------------------"')
            print('Patch column has now been added with "Default Patch"')
            print('Advise client to add patch details in next data extract."')
            print('-------------------------------------------------------------"')
        else:
            df[h] = ''
            print('-----------------------------------------------------------------------------------------------"')
            print ('Added header: ' + h + ' please check the correct data is appearing under this header.')
            print('-----------------------------------------------------------------------------------------------"')


def account_validation(file, df):
    ''' Validation specific to rent.accounts, checks for value
        in LocalAuthority field if null then it will fill default data.
        CURRENT NOT IN USE
    '''
    if ('acc' in file.lower()):
        df.loc[(df.LocalAuthority == '') | (df.LocalAuthority == 'Unknown') | (df.LocalAuthority == 'NULL'), 'LocalAuthority'] = "Default HB Cycle"
        print('------------------------------------------------------------"')
        print('"Default HB Cycle" was added where LocalAuthority = ''.')
        print('------------------------------------------------------------"')
        # try catch added if NeedsCategory doesn't exist it will create the column with a default value
        try:
            df.loc[(df.NeedsCategory == ''|""|" "),'NeedsCategory'] = "Default Data"
        except: 
            df['NeedsCategory'] = ''
            df.loc[(df.NeedsCategory == ''),'NeedsCategory'] = "Default Data"
            print('NeedsCategory column has now been added with default value')

def check_row_length(delimiter, file, list_of_column_names):
    ''' Finds the number of columns, Compares number to the no. of Rows
        Flags if there's a mismatch so you can inspect the lines in the file.
        Can Continue program or terminate if issues found.
    '''
    bad_columns = 0
    column_length = len(list_of_column_names)
    with open(file, newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if len(row) == 0:
                continue
            elif len(row) < column_length:
                print ('Columns Expected = ' + str(column_length) + ', Actual Columns = ' + str(len(row)) + '. Line number: ' + str(reader.line_num))
                bad_columns =+1
            elif len(row) > column_length:
                print ('Columns Expected = ' + str(column_length) + ', Actual Columns = ' + str(len(row)) + '. Line number: ' + str(reader.line_num))
                bad_columns =+1

    if (bad_columns >= 1):
        print('*********************************************************************************************************************************************************')
        menu_choice = input('Check the files output and fix those before you proceed with cleanse, You can override this by pressing y or Y or press anything to exit and review file.')
        print('*********************************************************************************************************************************************************')
        if menu_choice.lower() != 'y':
            print('*************************')
            sys.exit('Program now terminated')

def transform_dataframe(file, df):
    ''' Takes out commas, nulls, apostrophe values from the data.
    '''
    #load CSV as panda dataframe - converters keeps padding in accountReference
    print(df.head(10))
    #delete all commas in the dataframe and replace with null
    df.replace(',','', regex = True, inplace = True)
    print('---------------------------------------"')
    print ('Replaced all commas with null value.')
    #delete all commas in the dataframe and replace with null
    df.replace("'",'', regex = True, inplace = True)
    print ('Replaced all apostrophes with null value.')
    df.replace('NULL','', regex = True, inplace = True)
    df.replace('null','', regex = True, inplace = True)
    print ('Replaced the word null with empty value.')
    print('---------------------------------------"')

def date_parserv2(df):
    #Timestamp('2262-04-11 23:47:16.854775807') limitation for year in Pandas library
    ''' Finds all columns with 'date' within them. Gathers them into a list and parses into
        date format YYYY-MM-DD. Please note: Due to dt.strftime('%Y-%m-%d') the date field
        is turned into a str. If you need to do anything with the dates do them before
        string formatting.
    '''
    date_columns = []
    column_headers = list(df.columns.values)
    for column in column_headers:
        if 'date' in column.lower():
            date_columns.append(column)
        else:
            next
    if len(date_columns) > 0:
        print ('Date fields to parse: ' + str(date_columns))
        for to_parse in date_columns:
            #Convert date into DD-MM-YYYY format for Rentsense
            print('Parsed ' + to_parse + ' into date value.')          
            df[to_parse] = pd.to_datetime(df[to_parse], dayfirst=True)
            df[to_parse] = df[to_parse].dt.strftime('%Y-%m-%d')
    else:
        print('----------------------------"')
        print('No date columns to parse.')
        print('----------------------------"')
def get_current_date():
    ''' Used for writing into the filename.'''
    date = datetime.date(datetime.now())
    date = date.strftime('%Y%m%d')
    return date

def write_to_csv(filename, df):
    ''' Checks if "Cleaned Files" directory exists, if doesn't will create.
        Writes filename using current date and correct filename. Encoding: UTF-8
    '''
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
    file_to_write = filename + str(get_current_date()) + '.csv'
    df.to_csv(file_to_write, encoding ='utf-8', index = False)
    print('------------------------------------------------------------"')
    print(str(time.process_time()) + ' seconds taken to clean feed.')
    os.chdir(existingPath)
    return file_to_write

def controller(file_contains, filename_write):
    file = auto_detected_file(file_contains)
    delimiter = auto_detected_delimiter(file)
    headers_list = get_headers(delimiter, file)
    check_row_length(delimiter, file, headers_list)
    missing_headers, rename_headers = check_required_headers(headers_list, file)
    df = initialise_dataframe(file, delimiter)
    headers_rename(rename_headers,df)
    add_missing_headers(missing_headers, df)
    transform_dataframe(file, df)
    date_parserv2(df)
    file_name = write_to_csv(filename_write, df)
    print(file_name + ': Data transformation complete.')
    print('------------------------------------------------------------"')

def controller_all_files():
    list_of_files = []
    files_dictionary = auto_detected_all_files()
    for f in files_dictionary:
        file = f
        delimiter = auto_detected_delimiter(file)
        headers_list = get_headers(delimiter, file)
        check_row_length(delimiter, file, headers_list)
        missing_headers, rename_headers = check_required_headers(headers_list, file)
        df = initialise_dataframe(file, delimiter)
        headers_rename(rename_headers,df)
        add_missing_headers(missing_headers, df)
        transform_dataframe(file, df)
        date_parserv2(df)
        file_name = write_to_csv(files_dictionary[f], df)
        list_of_files.append(file_name)
    print('------------------------------------------------------------"')
    for f in list_of_files:
        print(f + ': Data transformation complete.')
    print('------------------------------------------------------------"')
if __name__ == "__main__":
    main()
