# Extract soils information from Esri

### Addresses [ticket #144](https://github.com/NCRN/NCRN_DM/issues/144)

### Repo contents
- `main.py` is the scripted workflow that addresses  that executes calls methods from `ssurgo.py`
- `ssurgo.py` holds classes and methods for `main.py`
- `requirements.txt` holds python package requirements to execute `main.py`
- `data/iss144_ssurgo.xlsx` is the source data file that `main.py` reads, parses, and builds a log file (via `write_huc()`) from

### Soils Data Source
[Esri Soils Data Application Link with Metadata](https://www.arcgis.com/home/item.html?id=cdc49bd63ea54dd2977f3f2853e07fff)
The data are downloadable as Esri packages based on 8-digit HUC.
Example endpoint:
[8-digit HUC for Middle Potomac Anacostia Occoquan](https://soilspackage-useast.s3.amazonaws.com/2021/MiddlePotomacAnacostiaOccoquan_02070010.ppkx)

### List of 8-Digit HUCs to Download (one Esri Package for each)
|  HUC8  |  Name  |
|  ------  | ------  | 
|  02070008  |  Middle Potomac-Catoctin  |
|  02070010  |  Middle Potomac-Anacostia-Occoquan  |
|  02060006  |  Patuxent  |
|  02070009  |  Monocacy  |
|  02070001  |  South Branch Potomac  |
|  02060003  |  Gunpowder-Patapsco  |
|  02070002  |  North Branch Potomac  |
|  05020006  |  Youghiogheny  |
|  02070007  |  Shenandoah  |
|  02070004  |  Conococheague-Opequon  |
|  02070011  |  Lower Potomac  |
|  02070006  |  North Fork Shenandoah  |
|  02070003  |  Cacapon-Town  |

### References for the Existing NCRN IMD Monitoring Site Locations Data
These data are stored in this File Geodatabase in OneDrive located here:
[\NCRN Data Management - Documents\Geospatial\GIS\Geodata\NCRN\NCRN_Monitoring_Locations.gdb](https://doimspp.sharepoint.com/:f:/r/sites/NCRNDataManagement/Shared%20Documents/Geospatial/GIS/Geodata/NCRN/NCRN_Monitoring_Locations.gdb?csf=1&web=1&e=pY4O8x)

### References for the Existing GIS Download Workflow

- [ ] Update the GIS Data Sources Excel Catalog to have all the 8-digit soil file endpoints. [NCRN_GIS_Data_Sources.xlxs](https://doimspp.sharepoint.com/:x:/r/sites/NCRNDataManagement/Shared%20Documents/Geospatial/NCRN_GIS_Data_Sources.xlsx?d=w852f91eadf32404e9ef012d5bc53015d&csf=1&web=1&e=J70zsT)
- [ ] Use the downloader script to get these downloaded to HUC-8 folders - writing them to this directory:
#### \DOI\NCRN Data Management - Documents\Geospatial\GIS\Geodata\Basedata\Vector\Soil\SSURGO
There would be 13 new folders each named with the full 8-digit HUC code.
[Directory to create folders in](https://doimspp.sharepoint.com/:f:/r/sites/NCRNDataManagement/Shared%20Documents/Geospatial/GIS/Geodata/Basedata/Vector/Soil/SSURGO?csf=1&web=1&e=gubg7M)

### Current Downloader Script
https://github.com/NCRN/NCRN_Geospatial/blob/main/Downloading/downloadData_v4.py 

### Steps After Getting the Data Download

- [ ] Unpack the Esri packages (.ppkx) to the same HUC folders that they are within
- [ ] Create a GDB to store a merged feature class of the soils
    - [ ] GDB can be stored in the root of the SSURGO folder and named: SSURGO_Esri.gdb 
- [ ] Merge the soils feature classes from the 13 extracted GDBs taken out of the .ppkx files so we have a "full region" soils file and the spatial join (or other method) can be done once on a master region-wide soils dataset
    - [ ] Name the feature class SSURGO_Esri.gdb\Mapunits
- [ ] Spatial join (or other "point-in-polygon" tool) the "master" soils dataset to the NCRN IMD ECO_MonitoringLocations_pt (IMLOCID) and ECO_MonitoringLocationsData_pt (DATAIMLOCID)
- [ ] Delete extra spatial join fields - we only need the IMLOCID and/or DATAIMLOCID to be retained in the derived datasets

# End Goal
Have two different tables (not a feature class - we don't need the geometry of the soils data) that contain the soil attributes from the Esri SSURGO dataset and are joinable by either IMLOCID or DATAIMLOCID (depending on the spatial dataset):

1. ECO_MonitoringLocations_EsriSSURGO_tbl
2. ECO_MonitoringLocationsData_EsriSSURGO_tbl

![image](https://user-images.githubusercontent.com/16828489/223487995-6be35133-e65c-4518-b3be-50d91704a7b8.png)






























































