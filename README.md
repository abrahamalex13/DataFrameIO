# DataFrameIO

## DataFrameWriter

For "average" DataFrame writes, _one_ interface
should deliver a write to either S3 or local, 
as well as csv or pickle. In particular,
seek to encapsulate S3 writes' boilerplate.

```
import DataFrameIO as dfio

df_writer = dfio.DataFrameWriter(
    dir=os.environ.get("DIR_S3_TARGET")
    , filename="dummy"
    , extensions=['csv']
    )
df_writer.write()

```

## DataFrameReader

For average DataFrame reads, _one_ interface
should encapsulate S3 boilerplate.

```
import DataFrameIO as dfio

df_reader = dfio.DataFrameReader(
    dir=os.environ.get("DIR_S3_TARGET")
    , filename="dummy"
    )
df = df_reader.read()

```
