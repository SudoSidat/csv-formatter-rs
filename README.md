# csv-formatter-rs

## General info
```
This Python script transforms CSV data feeds for Rentsense into the correct format.
It uses the Pandas library to read the data and do the following:

* Removes whitespaces and other characters which could cause issues when processing.
* Checks for required data feed headers, adds in if not there.
* Parses any date field into YYYY/MM/DD format.
* Check each row of data to make sure there is complete data.
* Adds in default values for certain columns if null.


## Pre-Requisites/Setup
```
To run this project, install Pandas & detect_delimiter using pip.

pip install Pandas
pip instal detect_delimiter

```

## Usage
python csv-formatter-rs.py



