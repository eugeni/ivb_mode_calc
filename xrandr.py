#!/usr/bin/python
#
# parses xrandr output for valid modes to use
# with IVB 3 display pipes
#
# The trick is that the pipes connected to both HDMI
# or DP outputs must use same resolution and refresh rate
#

import re
import os

valid_outputs = ["HDMI", "DP"]
resolution_r = re.compile("^(\d+)x(\d+)")

outputs = {}

data = os.popen("xrandr").readlines()
connector=None
for line in data:
    # scan xrandr output and search for HDMI or DP outputs
    line = line.strip()
    for output in valid_outputs:
        if line[:len(output)] == output:
            # found an output
            connector = line.split()[0]
            outputs[connector] = []
            continue
    match = re.match(resolution_r, line)
    if not match:
        continue
    if not connector:
        continue
    fields = line.split()
    resolution = fields[0]
    for rate in fields[1:]:
        rate = rate.replace("+", "").replace("*", "")
        mode = "%s --rate %s" % (resolution, rate)
        outputs[connector].append(mode)

for output in outputs.keys():
    if len(outputs[output]) == 0:
        del outputs[output]

results = []
for output1 in outputs:
    for mode1 in outputs[output1]:
        for output2 in outputs:
            if output1 == output2:
                continue
            for mode2 in outputs[output2]:
                if mode1 == mode2:
                    results.append("--output %s --mode %s --output %s --mode %s" % \
                            (output1, mode1, output2, mode2))
                    continue

if len(results) == 0:
    print "No valid modes for 3 display outputs"
else:
    print "Valid modes for 3 display outputs:"
    # now print the final results
    for valid_mode in results:
        print valid_mode
