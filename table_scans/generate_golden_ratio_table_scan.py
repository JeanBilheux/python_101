import pandas as pd
import numpy as np
import os

title = "Concrete_resonance_CT"
notes = "10mm Pb full filter 12mm Ni aperture shutter 1e-6 750e-6 3 0.16"
motor1 = "BL3:Mot:imageRot"
delay = 1
mcp_acquire = 1
mcp_file = "C:\Oct2018\IPTS-20740\October11_2018\Concrete_resonance_CT"
wait_for_what = "pCharge"
pcharge_value = 6  # coulomb
table_scan_file_name, ext = os.path.splitext(os.path.basename(__file__))
table_scan_file_name += ".csv"

golden_ratio_file = "golden_ratio_360degrees_500projections.csv"

# No editing after this line

df = pd.read_csv(golden_ratio_file)
list_golden_ratio_angles = np.array(df['angles'])

# first row
table = [["Title", "Notes", "MCPFile", motor1, "Delay", "MCPAcquire", "Wait For", "Value", "Or Time", "MCPAcquire"]]

for _angle in list_golden_ratio_angles:

    _str_angle = f"{_angle:.2f}"
    _new_str_angle = _str_angle.replace(".", "_")
    _row = [f"{title}", f"{notes}_{_new_str_angle}", f"{mcp_file}_{_new_str_angle}", float(f"{_angle}"), delay, 1, "pCharge", pcharge_value, "", 0]
    table.append(_row)

# export table scan csv file
df_out = pd.DataFrame(table)
df_out.to_csv(table_scan_file_name, index=False, header=False)
