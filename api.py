'''
En este script irá el backend de la aplicación, donde se subirán archivos a la nube
'''
from fastapi import FastAPI
import pandas as pd
import sqlite3 as sqlconn
import os
import sys

flux = FastAPI()

@flux.get("/")
def index():
    return "Hello World"

#TO-DO: implementar funciones de subida de archivos a la nube