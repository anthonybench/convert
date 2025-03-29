from pathlib import Path, PurePosixPath
import pandas as pd
from typing import List, Tuple
from rich import print
from sleepyconvert_toolchain.params import *


def readData(format:str, path:str) -> pd.DataFrame:
  '''dispatch table to read data file according to file extension'''
  return {
    'csv':pd.read_csv,
    'json':pd.read_json,
    'parquet':pd.read_parquet,
    'pkl':pd.read_pickle,
    'xlsx':pd.read_excel,
  }[format](path)


def writeData(df:pd.DataFrame, format:str, path:str, compress:bool) -> None:
  '''dispatch table to write data file according to file extension'''
  dispatch = {
    'csv':df.to_csv,
    'json':df.to_json,
    'parquet':df.to_parquet,
    'pkl':df.to_pickle,
    'xlsx':df.to_excel,
  }
  if compress:
    dispatch[format](f'{path}.gz', compression='gzip')
  else:
    dispatch[format](path)


def verifyPaths(input_path:str, output_path:str, supported_formats:List[str]) -> Tuple[str, str]:
  '''check if input and output paths are valid, pass back formats'''
  path_object = Path(input_path)
  input_format = PurePosixPath(input_path).suffix.lower()[1:]
  output_format = PurePosixPath(output_path).suffix.lower()[1:]
  if not path_object.exists():
    print(f'Error. Path {input_path} does not exist.')
    return '', ''
  elif not path_object.is_file():
    print(f'Error. Path {input_path} is not a file.')
    return '', ''
  elif input_format not in supported_data_formats:
    print(f'Error. Input format "{input_format}" not supported, must be one of: {", ".join(supported_data_formats)}')
    return '', ''
  elif output_format not in supported_data_formats:
    print(f'Error. Output format "{output_format}" not supported, must be one of: {", ".join(supported_data_formats)}')
    return '', ''
  return input_format, output_format
