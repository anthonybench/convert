from pathlib import Path, PurePosixPath
import pandas as pd
from typing import List, Tuple
from rich import print
from PIL import Image
from sleepyconvert_toolchain.params import *


def errorMessage(message:str) -> None:
  '''log error message'''
  print(f'[bold][red]Error[/bold]. {message}[/red]')


def successMessage(input_path:str, output_path:str, compress:bool) -> None:
  '''log success message'''
  output_path_display = f'{output_path}.gz' if compress else output_path
  print(f'✅ Converted [bold green]{input_path}[/bold green] ──▶ [bold green]{output_path_display}[/bold green]')


def verifyPaths(input_path:str, output_path:str, supported_formats:List[str]) -> Tuple[str, str]:
  '''check if input and output paths are valid, pass back formats'''
  path_object = Path(input_path)
  input_format = PurePosixPath(input_path).suffix.lower()[1:]
  output_format = PurePosixPath(output_path).suffix.lower()[1:]
  if not path_object.exists():
    errorMessage(f'Path {input_path} does not exist.')
    return '', ''
  elif not path_object.is_file():
    errorMessage(f'Path {input_path} is not a file.')
    return '', ''
  elif input_format not in supported_formats:
    errorMessage(f'Input format "{input_format}" not supported, must be one of: {", ".join(supported_formats)}')
    return '', ''
  elif output_format not in supported_formats:
    errorMessage(f'Output format "{output_format}" not supported, must be one of: {", ".join(supported_formats)}')
    return '', ''
  elif input_format == output_format:
    errorMessage(f'Input and output formats are the same: {input_format}')
  return input_format, output_format


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


def convertPNGtoJPG(png_path:str, jpg_path:str, quality:int=100) -> None:
  """converts a PNG image to JPG format"""
  img = Image.open(png_path)
  if img.mode == "RGBA":
    img = img.convert("RGB")
  img.save(jpg_path, "JPEG", quality=quality)


def convertJPGtoPNG(jpg_path:str, png_path:str) -> bool:
  """converts a JPG image to PNG format"""
  img = Image.open(jpg_path)
  img.save(png_path, "PNG")
