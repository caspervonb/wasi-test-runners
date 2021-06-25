import glob
import json
import subprocess
import sys
import os

command = sys.argv[1]

output = subprocess.check_output([command, "-V"])
output = output.decode("utf-8")
output = output.rstrip("\n")

(runtime_name, runtime_version) = tuple(output.split(" "))

results = []
for filepath in glob.glob("tests/*/*.wasm"):
    process = subprocess.run(["tools/wasm-test", command, filepath],
            capture_output=True, text=True)

    name = os.path.relpath(filepath, os.path.join(os.curdir, "tests"))

    status = None
    if process.returncode == 0:
        status = "PASS"
    else:
        status = "FAIL"

    message = process.stdout

    results.append({
      'name': name,
      'status': status,
      'message': message,
    })


print(json.dumps({
  'runtime': {
      'name': runtime_name,
      'version': runtime_version,
  },
  'results': results,
}, sort_keys=True, indent=2))
