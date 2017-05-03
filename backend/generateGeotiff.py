
# TODO almost everything

src_ds = gdal.Open( src_filename )
dst_ds = driver.CreateCopy( dst_filename, src_ds, 0 )
# Once we're done, close properly the dataset
dst_ds = None
src_ds = None
