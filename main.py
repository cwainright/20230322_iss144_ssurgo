# a procedure that downloads soil ssurgo data, parses data, saves files
# https://github.com/NCRN/NCRN_DM/issues/144

import ssurgo
import os
import arcpy
from importlib import reload
reload(ssurgo)
# myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
# myhuc = ssurgo.Huc(filename='data/test.xlsx', VERBOSE=True)
# myhuc.build_urls()
# myhuc.write_huc(out_file='data/test.xlsx')
# myhuc.download(save_directory='data')
# myhuc.download(save_directory=r'C:\Users\cwainright\OneDrive - DOI\Documents - NCRN Data Management\Geospatial\GIS\Geodata\Basedata\Vector\Soil\SSURGO')
# myhuc.write_huc(out_file='data/log.xlsx') # start log file

# myhuc.save_huc(filename='data/myhuc')
# del myhuc
myhuc = ssurgo.open_huc(filename='data/myhuc')
# myhuc.unpack()
# myhuc.save_huc(filename='data/myhuc')
# myhuc.write_huc(out_file='data/testlog.xlsx') # update log file
filename = 'test.gdb'
file_dir = os.path.join(os.getcwd(), 'data')
# myhuc.huc_data["gdb"] = os.path.join(file_dir, filename)
myhuc.merge(filename=filename, file_dir=file_dir)
# myhuc.write_huc(out_file='data/testlog.xlsx') # update log file
# myhuc.save_huc(filename='data/myhuc')
























































arcpy.env.workspace = r'data\test.gdb'
# datasets = arcpy.ListDatasets(feature_type='feature')
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)


























targets = []
for dir in range(0, myhuc.huc_data.shape[0]):
    target = os.path.join(myhuc.huc_data["unpack_dir"][dir], 'p20')
    for file in os.listdir(target):
        if file.endswith('.gdb'):
            target = os.path.join(target, file)
    targets.append(target)

for gdb in targets:
    arcpy.env.workspace = gdb
    datasets = arcpy.ListDatasets()
    datasets = [''] + datasets if datasets is not None else []

    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            path = os.path.join(arcpy.env.workspace, ds, fc)
            print(path)

arcpy.env.workspace = r'data\02070008\MiddlePotomacCatoctin_02070008\p20\middlepotomaccatoctin_02070008.gdb'
# datasets = arcpy.ListDatasets(feature_type='feature')
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)