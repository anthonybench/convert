# **sleepyconvert**
*A quick way to convert file formats.*

<br />

## **Welcome to sleepyconvert!**
Do you find yourself bookmarking various online converters or having several tools to convert common file types? I did, and it didn't spark joy.

**`sleepyconvert`** is a tool that handles this in a minimal syntax.

Quickly convert file formats to and from:
- **data**
  - `csv`
  - `parquet`
  - `json`
  - `pkl`
  - `xlsx`
- **img**
  - `png`
  - `jpg`/`jpeg`
- **doc**
  - TODO: not yet implemented

For some data files, you can optionally compress (*gzip*) the output.

> ℹ️ Note that this tool presumes format by file extension. If you leave out extensions, or give csv data a `.json` extension for funsies, then you're being silly.

<br />

## **Get Started 🚀**
<hr>

```sh
pip install sleepyconvert
pip install --upgrade sleepyconvert

python -m sleepyconvert data data.csv data.parquet --compress
python -m sleepyconvert --help
```

<br />

## **Usage ⚙**
<hr>

Set a function in your shell environment to run a script like:
```sh
alias convert='python -m sleepyconvert'
```

Presuming you've named said macro `convert`, print the help message:
```sh
convert --help
convert data data.csv data.parquet
convert img selfie.jpg selfie.png
```

<br />

## **Technologies 🧰**
<hr>

  - [Pandas](https://pandas.pydata.org/docs/)
  - [Typer](https://typer.tiangolo.com/)
  - [PyArrow](https://arrow.apache.org/docs/python/index.html)
  - [openpyxl](https://pypi.org/project/openpyxl/)

<br />

## **Contribute 🤝**
<hr>

If you have thoughts on how to make the tool more pragmatic, submit a PR 😊.

To add support for more data/file types:
1. append extension name to `supported_<mode>_formats` in `sleepyconvert_toolchain.params.py`
2. add detection logic branch to the `main` function in `sleepyconvert_toolchain/commands.py`
3. update this readme

<br />

## **License, Stats, Author 📜**
<hr>

<img align="right" alt="example image tag" src="https://i.imgur.com/ZHnNGeO.png" width="200" />

<!-- badge cluster -->
![PyPI - License](https://img.shields.io/pypi/l/sleepyconvert?style=plastic)
![PyPI - Version](https://img.shields.io/pypi/v/sleepyconvert)
![GitHub repo size](https://img.shields.io/github/repo-size/anthonybench/convert)
<!-- / -->

See [License](LICENSE) for the full license text.

This package was authored by *Isaac Yep*.