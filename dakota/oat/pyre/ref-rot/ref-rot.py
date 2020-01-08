import input as inp
import glob
import subprocess
import dakota.interfacing as di
import sys
import os
sys.path.append('../../../../scripts')

cycdir = '../../../../cyclus-files/oat/pyre/ref-rot/'

# ----------------------------
# Parse Dakota parameters file
# ----------------------------

params, results = di.read_parameters_file()

# -------------------------------
# Convert and send to Cyclus
# -------------------------------

# Edit Cyclus input file
cyclus_template = cycdir + 'ref-rot.xml.in'
scenario_name = 'rot' + str(int(params['rot']))  # + '-exp'
variable_dict = {'refining_rotation': int((params['rot']))}
output_xml = cycdir + 'ref-rot.xml'
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
