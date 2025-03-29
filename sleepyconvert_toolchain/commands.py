from sys import exit
from rich import print
import typer
from sleepyconvert_toolchain.params import *
from sleepyconvert_toolchain.utils import *

app = typer.Typer(help="Convert common filetypes and data formats quickly.")


@app.command()
def data(input_path:str, output_path:str, compress:bool=False):
  '''Convert data file from one format to another, optionally compressing output.'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_data_formats)
  if not (input_format and output_format):
    exit(1)
    
  # additional guards
  if input_format == output_format:
    print(f'Input and output formats are the same: {input_format}')
    exit(1)
  if compress and output_format == 'xlsx':
    print(f'Error. Cannot compress xlsx files. Please remove the --compress flag.')
    exit(1)

  # read
  try:
    df = readData(input_format, input_path)
  except Exception as e:
    print(f'Error reading data:\n{e}')

  # write
  try:
    writeData(df, output_format, output_path, compress)
  except Exception as e:
    print(f'Error writing data:\n{e}')

  # log
  output_path_display = f'{output_path}.gz' if compress else output_path
  print(f'✅ Converted [bold green]{input_path}[/bold green] ──▶ [bold green]{output_path_display}[/bold green]')


@app.command()
def img(input_path:str, output_path:str, compressed:bool=False):
  '''Convert image file from one format to another'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_img_formats)
  if not (input_format and output_format):
    exit(1)

  # read
  try:
    pass # TODO: parse image into object
  except Exception as e:
    print(f'Error reading image:\n{e}')

  # write
  try:
    pass # TODO: write image object to file
  except Exception as e:
    print(f'Error writing image:\n{e}')


@app.command()
def doc(input_path:str, output_path:str):
  '''Convert document file from one format to another'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_doc_formats)
  if not (input_format and output_format):
    exit(1)

  # read
  try:
    pass # TODO: parse image into object
  except Exception as e:
    print(f'Error reading image:\n{e}')

  # write
  try:
    pass # TODO: write image object to file
  except Exception as e:
    print(f'Error writing image:\n{e}')
