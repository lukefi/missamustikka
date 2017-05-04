from osgeo import gdal, ogr, gdalconst

gdal.UseExceptions()
gdal.AllRegister()

src_filename = "../../aineisto/Clc2012_FI20m_Espoo.tif"
dstPath = "../../output"
berries = ["mustikka", "puolukka", "karpalo"]

# WARNING: these values are for testing only, not real data
corineToBerryIndex = dict()
corineToBerryIndex["mustikka"] = dict()
corineToBerryIndex["mustikka"][24] = 70
corineToBerryIndex["mustikka"][25] = 80
corineToBerryIndex["mustikka"][27] = 50
corineToBerryIndex["mustikka"][28] = 60
corineToBerryIndex["puolukka"] = dict()
corineToBerryIndex["puolukka"][24] = 60
corineToBerryIndex["puolukka"][25] = 50
corineToBerryIndex["karpalo"] = dict()
corineToBerryIndex["karpalo"][40] = 50
corineToBerryIndex["karpalo"][42] = 80

src_ds = gdal.Open(src_filename)
corineBand = src_ds.GetRasterBand(1)
xSize = corineBand.XSize
ySize = corineBand.YSize
print xSize, ySize

for berry in berries:
	driver = src_ds.GetDriver()
	dst_ds = driver.Create(dstPath + "/" + berry + ".tif", xSize, ySize, 1, gdal.GDT_UInt16)
	dst_ds.SetGeoTransform(src_ds.GetGeoTransform())
	dst_ds.SetProjection(src_ds.GetProjection())

	array = corineBand.ReadAsArray(0, 0, xSize, ySize)

	for x in range(0, xSize):
		for y in range(0, ySize):
			origVal = array[y,x]
			if origVal in corineToBerryIndex[berry]:
				finalVal = corineToBerryIndex[berry][origVal]
			else:
				finalVal = 0
			array[y,x] = finalVal
	print array

	dstBand = dst_ds.GetRasterBand(1)
	dstBand.WriteArray(array, 0, 0)

	# Once we're done, close properly the dataset
	dstBand = None
	dst_ds = None

corineBand = None
src_ds = None
