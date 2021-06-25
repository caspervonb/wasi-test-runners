import glob
import json
import subprocess
import sys
import os

command = sys.argv[1]
runtime = subprocess.check_output([command, "-V"]).decode("utf-8").rstrip('\n') 

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
  'runtime': runtime,
  'results': results,
}, sort_keys=True, indent=2))
