import sys, os
"""
Simply writes a text content (used in other python scripts for speed up.
Since text might have spaces, we have convention to add _^_^_ as space
"""

text = sys.argv[1].strip().replace("_^_^_", " ")
output_path = os.path.abspath(sys.argv[2])

with open(output_path, "w") as writer:
    writer.write(text)