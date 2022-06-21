from dotenv import load_dotenv
import os

from DataFrameIO.DataFrameReader import DataFrameReader

load_dotenv()

def test_read_csv_from_s3():

    df_reader = DataFrameReader(
        dir=os.environ.get("DIR_S3_TARGET")
        , filename="dummy"
        )
    df = df_reader.read()

    assert df is not None