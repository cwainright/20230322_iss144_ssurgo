# a procedure that downloads soil ssurgo data, parses data, saves files
# https://github.com/NCRN/NCRN_DM/issues/144

import ssurgo
import os
import arcpy
from importlib import reload
import re
reload(ssurgo)

# myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
myhuc = ssurgo.Huc(filename='data/test.xlsx', VERBOSE=True)
myhuc.build_urls()
myhuc.write_huc(out_file='data/test.xlsx')
myhuc.download(save_directory='data')
# myhuc.download(save_directory=r'C:\Users\cwainright\OneDrive - DOI\Documents - NCRN Data Management\Geospatial\GIS\Geodata\Basedata\Vector\Soil\SSURGO')
myhuc.write_huc(out_file='data/log.xlsx') # start log file

# myhuc.save_huc(filename='data/myhuc')
# del myhuc
myhuc = ssurgo.open_huc(filename='data/myhuc')
# myhuc.unpack()
# myhuc.save_huc(filename='data/myhuc')

# myhuc.write_huc(out_file='data/testlog.xlsx') # update log file
# filename = 'test.gdb'
# file_dir = os.path.join(os.getcwd(), 'data')
# myhuc.merge(filename=filename, file_dir=file_dir)

# prove that `merge()` worked
arcpy.env.workspace = r'data\test.gdb'
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)

# myhuc.write_huc(out_file='data/testlog.xlsx') # update log file
# myhuc.save_huc(filename='data/myhuc')

# `join()`
myhuc.join(
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocations_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits'),
    out_feature='data/test.gdb/join_output'
)


os.path.join(os.getcwd(), 'data/test.gdb/Mapunits')


os.path.split('data/test.gdb/Mapunits')











































































os.path.normpath(r'C:\Users\cwainright\OneDrive - DOI\Documents\data_projects\2023\20230322_iss144_ssurgo\data\NCRN_Monitoring_Locations.gdb\IMD\ECO_MonitoringLocationLogistics_py')
mystring = os.path.split("data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt")[0]
re.search('(^.*[/$])', mystring)
re.search('(^.*[/$])', mystring)

os.path.join(os.getcwd(), *os.path.split(re.search('(?:(?!/IMD).)*', mystring)[0]))



mystring = os.path.join(os.getcwd(), "data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocations_pt")
myanswer = re.search('(?:(?!NCRN).)*', mystring)
myanswer[0]

arcpy.env.workspace = os.path.split("data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt")[0]
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []

paths = []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        paths.append(path)

'data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt' in paths





target_features = "data/test.gdb/Mapunits"
join_features = "data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt"
out_feature_class = "data/test.gdb/testjoin1"
arcpy.analysis.SpatialJoin(target_features, join_features, out_feature_class)

target_features = "data/test.gdb/testjoin1"
join_features = "data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocationsData_pt"
out_feature_class = "data/test.gdb/testjoin2"
arcpy.analysis.SpatialJoin(target_features, join_features, out_feature_class)





os.path.split("data/NCRN_Monitoring_Locations.gdb/IMD/ECO_MonitoringLocations_pt")[0]












arcpy.env.workspace = r'data\NCRN_Monitoring_Locations.gdb'
# datasets = arcpy.ListDatasets(feature_type='feature')
datasets = arcpy.ListDatasets()
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)
