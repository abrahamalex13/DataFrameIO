import pandas as pd
import boto3

from DataFrameIO import utils


class DataFrameReader:
    """
    Single interface for reading rectangular data.
    Core functionality is read from S3 because
    local (pandas) reads involve already-clean interface.

    Parameters
    ----------
    dir : str
        Directory for file write(s), excluding ending delimiter. 
        If S3, prefix 's3:/'.
    filename : str
        Name for file read(s), excluding file extension.
    """
    def __init__(self, dir, filename):

        self.dir = dir
        if dir[0:3] == 's3:':
            self.dir_is_s3 = True
        else:
            self.dir_is_s3 = False

        self.filename = filename
        self.extension = 'csv'

        self.dir_clean, self.filename_clean = \
            utils.clean_path_components(dir, filename)

    def read(self):

        reader = self._get_reader()

        try:
            df = reader()
            df = utils.coerce_dtypes_datetime(df)
            print("File read succeeded: " + self.filename_clean)

        except:
            print("File read failed: " + self.filename_clean)
            df = None

        return df

    def _read_csv_from_s3(self):

        s3 = boto3.client("s3")
        response = s3.get_object(
            Bucket=self.dir_clean
            , Key=self.filename_clean + '.csv'
            )
        df = pd.read_csv(response.get("Body"))

        return df

    def _get_reader(self):

        if self.dir_is_s3:
            if self.extension == 'csv':
                return self._read_csv_from_s3
        else:
            return None
