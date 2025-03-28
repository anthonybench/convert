#!/usr/bin/env python
import pandas as pd
from pathlib import Path, PurePosixPath

'''README
Usage:
    ./data_conversion/convert_data.py

Adding format support:
    1. append `supported_formats`
    2. append `readData()`
    3. append `writeData()`

Dependencies:
    - pandas
    - openpyxl # for xlsx
    
TODO:
    - option to gzip the file
    - detection logic
    - better printing
'''


#───Params───────────────────
input_file = 'data_conversion/test_wide.csv'
output_file = 'data_conversion/test_wide.xlsx'
#
supported_formats = [
  'csv',
  'json',
  'parquet',
  'pkl',
  'xlsx',
]


#───Guards───────────────────
path_object = Path(input_file)
input_format = PurePosixPath(input_file).suffix.lower()[1:]
output_format = PurePosixPath(output_file).suffix.lower()[1:]
if not path_object.exists():
    print(f'Error. Path {input_file} does not exist.')
    exit(1)
elif not path_object.is_file():
    print(f'Error. Path {input_file} is not a file.')
    exit(1)
elif input_format not in supported_formats:
    print(f'Error. Input format "{input_format}" not supported, must be one of: {", ".join(supported_formats)}')
    exit(1)
elif output_format not in supported_formats:
    print(f'Error. Output format "{output_format}" not supported, must be one of: {", ".join(supported_formats)}')
    exit(1)


#───Utils────────────────────
def readData() -> pd.DataFrame:
    '''dispatch table to read data file according to file extension'''
    return {
        'csv':pd.read_csv,
        'json':pd.read_json,
        'parquet':pd.read_parquet,
        'pkl':pd.read_pickle,
        'xlsx':pd.read_excel,
    }[input_format](input_file)

def writeData(df:pd.DataFrame) -> None:
    '''dispatch table to write data file according to file extension'''
    {
        'csv':df.to_csv,
        'json':df.to_json,
        'parquet':df.to_parquet,
        'pkl':df.to_pickle,
        'xlsx':df.to_excel,
    }[output_format](output_file)


#───Exec─────────────────────
# read
try:
    df = readData()
except Exception as e:
    print(f'Error reading data:\n{e}')

# write
try:
    writeData(df)
except Exception as e:
    print(f'Error writing data:\n{e}')
