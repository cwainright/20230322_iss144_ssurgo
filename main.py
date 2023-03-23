# a procedure that downloads soil ssurgo data, parses data, saves files
# https://github.com/NCRN/NCRN_DM/issues/144

import ssurgo
from importlib import reload
reload(ssurgo)
myhuc = ssurgo.Huc(filename='data/iss144_ssurgo.xlsx', VERBOSE=True)
# myhuc = ssurgo.Huc(filename='data/test.xlsx', VERBOSE=True)
myhuc.build_urls()
# myhuc.write_huc(out_file='data/test.xlsx')
# myhuc.download(save_directory='data')
myhuc.download(save_directory=r'C:\Users\cwainright\OneDrive - DOI\Documents - NCRN Data Management\Geospatial\GIS\Geodata\Basedata\Vector\Soil\SSURGO')
myhuc.write_huc(out_file='data/log.xlsx')