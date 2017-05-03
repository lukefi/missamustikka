from osgeo import gdal, ogr

src_filename = "../../aineisto/Clc2012_FI20m_Espoo.tif"
dst_filename = "../../output/mustikka.tif"

src_ds = gdal.Open(src_filename)
driver = src_ds.GetDriver()
dst_ds = driver.CreateCopy(dst_filename, src_ds, 0)

# TODO modify the destination dataset

# Once we're done, close properly the dataset
dst_ds = None
src_ds = None
