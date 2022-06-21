import pandas as pd
import re
import pathlib

def clean_path_components(dir, filename):
    """
    Clean path's directory and filename
    for DataFrameIO interfaces. 

    Clean directory with OS-specific delimiters;
    if S3, split into bucket name & subfolders.
    Correctly handle select input delimiters: "/", "//", "\\".

    Clean filename to have no extension. 
    If S3, prefix with bucket subfolders.

    Returns strings: simpler data types
    passing to boto, pandas write functions.
    """

    dir = object_transform_dir_input(dir)
    filename = drop_filename_ext(filename)

    # if local data save, align dir details to machine's OS
    if dir.parts[0] != 's3:':
        dir = dir.__str__()

    # if S3 data save, drop synthetic s3:/ prefix
    elif dir.parts[0] == 's3:':

        dir_parts_all = dir.parts

        dir = dir_parts_all[1]

        depth_hierarchy_dir = len(dir_parts_all) - 1

        if depth_hierarchy_dir > 1:
            folder_hierarchy_in_bucket = "/".join(dir_parts_all[2:])
            filename = folder_hierarchy_in_bucket + "/" + filename

    return dir, filename

def object_transform_dir_input(dir):
    return pathlib.PurePath(dir)

def drop_filename_ext(filename):
    return pathlib.PureWindowsPath(filename).stem


def coerce_dtypes_datetime(df):

    varnames_datetime = [
        x for x in df.columns 
        if re.search('date|created_at', x)
        ]

    if len(varnames_datetime) > 0:
        for x in varnames_datetime:
            df.loc[:, x] = pd.to_datetime(df[x])

    return df
