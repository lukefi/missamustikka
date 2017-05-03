from osgeo import gdal, ogr, gdalconst

gdal.UseExceptions()
gdal.AllRegister()

src_filename = "../../aineisto/Clc2012_FI20m_Espoo.tif"
dst_filename = "../../output/mustikka.tif"

# WARNING: these values are for testing only, not real data
corineToMustikka = dict()
corineToMustikka[24] = 80
corineToMustikka[25] = 70

src_ds = gdal.Open(src_filename)
driver = src_ds.GetDriver()

corineBand = src_ds.GetRasterBand(1)
xSize = corineBand.XSize
ySize = corineBand.YSize
print xSize, ySize

dst_ds = driver.Create(dst_filename, xSize, ySize, 1, gdal.GDT_UInt16)
dst_ds.SetGeoTransform(src_ds.GetGeoTransform())
dst_ds.SetProjection(src_ds.GetProjection())

array = corineBand.ReadAsArray(0, 0, xSize, ySize)

for x in range(0, xSize):
	for y in range(0, ySize):
		origVal = array[y,x]
		if origVal in corineToMustikka:
			finalVal = corineToMustikka[origVal]
		else:
			finalVal = 0
		array[y,x] = finalVal
print array

dstBand = dst_ds.GetRasterBand(1)
dstBand.WriteArray(array, 0, 0)

# Once we're done, close properly the dataset
dst_ds = None
src_ds = None
