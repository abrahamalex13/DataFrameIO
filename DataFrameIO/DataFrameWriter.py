import pandas as pd
from io import StringIO
import boto3
import os
import pathlib

from DataFrameIO import utils

class DataFrameWriter:
    """
    Interface for writing pandas DataFrame 
    to different environments, multiple files:
    locally or S3, csv or pkl.

    Parameters
    ----------
    dir : str
        Directory for file write(s), excluding ending delimiter. 
        If S3, prefix 's3:/', then bucket & subfolder name.
    filename : str
        Name for file write(s), excluding file extension.
    extensions : list
        Combination of ['csv', 'pkl'].
    """
    def __init__(self, dir: str, filename: str, extensions=['csv']):

        self.dir = dir
        if dir[0:3] == 's3:':
            self.dir_is_s3 = True
        else:
            self.dir_is_s3 = False

        self.filename = filename

        self.extensions = extensions

        self.dir_clean, self.filename_clean = \
            utils.clean_path_components(dir, filename)

        if not self.dir_is_s3:

            self.path_no_ext = \
                pathlib.Path(self.dir_clean) / self.filename_clean
            
    
    def write(self, df):

        for ext in self.extensions:

            writer = self._get_writer(ext)

            try:
                writer(df)
                response = {
                    'ok': True
                    , 'message': 'File written: ' + self.filename_clean 
                    }

            except FileNotFoundError:
                os.makedirs(self.dir_clean)
                try:
                    writer(df)
                    response = {
                        'ok': True
                        , 'message': 'File written: ' + self.filename_clean 
                        }
                except:
                    response = {
                        'ok': False
                        , 'message': 'File write failed: ' + self.filename_clean 
                        }
            
            # TODO: suppose error is not FileNotFoundError. What then?

        return response

    def _get_writer(self, extension):
        
        if self.dir_is_s3:
            if extension == 'csv':
                return self._write_csv_to_s3
        else:
            if extension == 'csv':
                return self._write_csv_to_local
            elif extension == 'pkl':
                return self._write_pkl_to_local

    def _write_csv_to_s3(self, df):

        file = StringIO()
        df.to_csv(file, index=False)

        s3 = boto3.resource('s3')
        s3 \
            .Object(self.dir_clean, self.filename_clean+'.csv') \
            .put(Body=file.getvalue())

    def _write_csv_to_local(self, df):
        df.to_csv(self.path_no_ext.with_suffix('.csv'), index=False)

    def _write_pkl_to_local(self, df):
        df.to_pickle(self.path_no_ext.with_suffix('.pkl'))
