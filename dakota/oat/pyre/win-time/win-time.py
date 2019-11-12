import glob
import subprocess
import dakota.interfacing as di
import sys
import os
sys.path.append('../../../../scripts')
import input as inp

cycdir = '../../../../cyclus-files/oat/pyre/win-time/'

# ----------------------------
# Parse Dakota parameters file
# ----------------------------

params, results = di.read_parameters_file()

# -------------------------------
# Convert and send to Cyclus
# -------------------------------

# Edit Cyclus input file
cyclus_template = cycdir + 'win-time.xml.in'
scenario_name = 'time' + str(int(params['time']))  # + '-exp'
variable_dict = {'win_time': int((params['time'])) / 10}
output_xml = cycdir + 'win-time.xml'
inp.render_input(cyclus_template, variable_dict, output_xml)

# Run Cyclus with edited input file
output_sqlite = cycdir + scenario_name + '.sqlite'
os.system('cyclus -i ' + output_xml + ' -o ' + output_sqlite)
# ----------------------------
# Return the results to Dakota
# ----------------------------

for i, r in enumerate(results.responses()):
    if r.asv.function:
        r.function = 1

results.write()
