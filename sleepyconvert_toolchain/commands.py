from sys import exit
from rich import print
import typer
from PIL import Image
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
  if compress and output_format == 'xlsx':
    errorMessage('Cannot compress xlsx files. Please remove the --compress flag.')
    exit(1)

  # read
  try:
    df = readData(input_format, input_path)
  except Exception as e:
    errorMessage(f'Error reading data:\n{e}')
    exit(1)

  # write
  try:
    writeData(df, output_format, output_path, compress)
  except Exception as e:
    errorMessage(f'Error writing data:\n{e}')
    exit(1)

  # log
  output_path_display = f'{output_path}.gz' if compress else output_path
  successMessage(input_path, output_path_display, compress)
  exit(0)


@app.command()
def img(input_path:str, output_path:str):
  '''Convert image file from one format to another'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_img_formats)
  if not (input_format and output_format):
    exit(1)

  # write
  match (input_format, output_format):
    case ('png', 'jpg'|'jpeg'):
      try:
        convertPNGtoJPG(input_path, output_path)
      except Exception as e:
        errorMessage(f'Error converting PNG to JPG:\n{e}')
        exit(1)
    case ('jpg'|'jpeg', 'png'):
      try:
        convertJPGtoPNG(input_path, output_path)
      except Exception as e:
        errorMessage(f'Error converting JPG to PNG:\n{e}')
        exit(1)

  # log
  successMessage(input_path, output_path, compress=False)
  exit(0)


@app.command()
def doc(input_path:str, output_path:str):
  '''Convert document file from one format to another'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_doc_formats)
  if not (input_format and output_format):
    exit(1)

  # TODO

  # log
  successMessage(input_path, output_path, compress=False)
  exit(0)