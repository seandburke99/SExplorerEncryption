#!/bin/bash
conda activate default

pyinstaller -F --hidden-import=_cffi_backend SExplorerEncryption.py