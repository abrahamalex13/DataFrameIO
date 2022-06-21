from DataFrameIO.utils import clean_path_components

def test_clean_dir_lead_dot():
    dir, filename = clean_path_components("./tests", "dummy_data.csv")
    assert dir == "tests"

def test_clean_dir_end_slashes():
    
    dir_end_slash1, filename = clean_path_components("tests/", "data")
    dir_end_slash2, filename = clean_path_components("tests//", "data")
    dir_end_backslash2, filename = clean_path_components("tests\\", "data")

    assert "tests" == dir_end_slash1 == dir_end_slash2 == dir_end_backslash2

def test_clean_dir_s3_slash_delims():

    dir_slash1, filename = clean_path_components("s3:/tests", "data")
    dir_slash2, filename = clean_path_components("s3://tests", "data")
    dir_backslash2, filename = clean_path_components("s3:\\tests", "data")

    assert "tests" == dir_slash1 == dir_slash2 == dir_backslash2

def test_clean_filename_s3_subfolder():

    dir, filename_slash1 = clean_path_components("s3:/tests/dev", "data")
    dir, filename_slash2 = clean_path_components("s3://tests//dev", "data")
    dir, filename_backslash2 = clean_path_components("s3:\\tests\\dev", "data")

    assert "dev/data" == filename_slash1 == filename_slash2 == filename_backslash2

def test_clean_filename_drop_ext():
    dir, filename = clean_path_components("./tests", "dummy_data.csv")
    assert filename == 'dummy_data'
