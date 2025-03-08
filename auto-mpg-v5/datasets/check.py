import os
import sys

status = os.system("b3sum -c blake3-checksum")
if status != 0:
    sys.exit("Error: invalid auto-mpg.parquet file")