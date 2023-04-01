# a procedure that downloads soil ssurgo data, parses data, saves files
# https://github.com/NCRN/NCRN_DM/issues/144

import ssurgo
import os
import arcpy
from importlib import reload
reload(ssurgo)

# a full test workflow
myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
myhuc.build_urls()
myhuc.download(save_directory='data')
myhuc.unpack()
filename = 'test.gdb'
file_dir = os.path.join(os.getcwd(), 'data')
myhuc.merge(filename=filename, file_dir=file_dir)
myhuc.join(
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocationsData_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
)
myhuc.convert()
myhuc.select()
input_user = os.path.join(os.getcwd(), 'data', 'mygdb.gdb')
myhuc.copy(save_dir=input_user)
myhuc.save_huc(filename='data/myhuc')
myhuc.write_huc(out_file='data/testlog.xlsx')


'''
# a part-length test workflow
myhuc = ssurgo.Huc(filename='data/test.xlsx', VERBOSE=True)
myhuc.build_urls()
myhuc.download(save_directory='data')
myhuc.unpack()
filename = 'test.gdb'
file_dir = os.path.join(os.getcwd(), 'data')
myhuc.merge(filename=filename, file_dir=file_dir)
myhuc.join(
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocationsData_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
)
myhuc.convert()
myhuc.select()
input_user = os.path.join(os.getcwd(), 'data', 'mygdb.gdb')
myhuc.copy(save_dir=input_user)
myhuc.save_huc(filename='data/myhuc')
myhuc.write_huc(out_file='data/testlog.xlsx')
'''

'''
# notes and test bits

# myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
myhuc = ssurgo.Huc(filename='data/test.xlsx', VERBOSE=True)
myhuc.build_urls()
# myhuc.write_huc(out_file='data/test.xlsx')
myhuc.download(save_directory='data')
# myhuc.download(save_directory=r'C:\Users\cwainright\OneDrive - DOI\Documents - NCRN Data Management\Geospatial\GIS\Geodata\Basedata\Vector\Soil\SSURGO')
# myhuc.write_huc(out_file='data/testlog.xlsx') # start log file

# myhuc.save_huc(filename='data/myhuc')
# del myhuc
# myhuc = ssurgo.open_huc(filename='data/myhuc')
myhuc.unpack()
# myhuc.save_huc(filename='data/myhuc')

# myhuc.write_huc(out_file='data/testlog.xlsx') # update log file
filename = 'test.gdb'
file_dir = os.path.join(os.getcwd(), 'data')

# `merge()`
myhuc.merge(filename=filename, file_dir=file_dir)
# prove that `merge()` worked
# arcpy.env.workspace = r'data\test.gdb'
# datasets = arcpy.ListDatasets()
# datasets = [''] + datasets if datasets is not None else []
# mydata = []
# for ds in datasets:
#     for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
#         path = os.path.join(arcpy.env.workspace, ds, fc)
#         print(path)
#         mydata.append(path)


# arcpy.env.workspace = os.path.join(os.getcwd(), r'data\test.gdb')
# arcpy.management.DeleteFeatures(os.path.join(os.getcwd(), r'data\test.gdb\join_output'))
# `join()`
myhuc.join(
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocations_pt"),
    os.path.join(os.getcwd(), r"data\\NCRN_Monitoring_Locations.gdb\\IMD\\ECO_MonitoringLocationsData_pt"),
    target_feature=os.path.join(os.getcwd(), r'data\test.gdb\Mapunits')
)
myhuc.convert()
myhuc.select()
myhuc.save_huc(filename='data/myhuc')
myhuc.write_huc(out_file='data/testlog.xlsx')

myhuc = ssurgo.open_huc(filename='data/myhuc')
myhuc.huc_data
input_user = os.path.join(os.getcwd(), 'data', 'mygdb3.gdb')
myhuc.copy(save_dir=input_user)
'''

