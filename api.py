'''
En este script irá el backend de la aplicación, donde se subirán archivos a la nube
'''
from fastapi import FastAPI
import pandas as pd
import sqlite3 as sqlconn
import os
import sys