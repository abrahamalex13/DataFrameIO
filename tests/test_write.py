from dotenv import load_dotenv
import os
import pandas as pd
import pathlib
import shutil

from DataFrameIO.DataFrameWriter import DataFrameWriter

load_dotenv()

df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})

def test_write_csv_to_local():

    df_writer = DataFrameWriter(
        dir="tests/dump", filename="dummy", extensions=['csv']
        )
    
    assert df_writer.write(df) == 200

def test_write_csv_to_local_mkdir():

    df_writer = DataFrameWriter(
        dir="tests/dump/temp", filename="dummy", extensions=['csv']
        )
    check = df_writer.write(df) == 200

    try:
        shutil.rmtree(pathlib.Path("./tests/dump/temp"))
    except:
        print("tests/dump/temp could not be deleted.")
    
    assert check

def test_write_pkl_to_local():

    df_writer = DataFrameWriter(
        dir="tests/dump", filename="dummy", extensions=['pkl']
        )
    
    assert df_writer.write(df) == 200

def test_write_csv_to_s3():

    df_writer = DataFrameWriter(
        dir=os.environ.get("DIR_S3_TARGET")
        , filename="dummy"
        , extensions=['csv']
        )

    assert df_writer.write(df) == 200
