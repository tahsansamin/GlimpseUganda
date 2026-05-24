import json

with open('eval_try.ipynb', 'r') as f:
    nb = json.load(f)

# Patch Cell 1 (index 1) to add time.sleep(4)
source = nb['cells'][1]['source']
new_source = []
for line in source:
    if "import requests" not in "".join(new_source) and "import time" not in "".join(new_source):
        # We will add import time at the top
        pass
    if line.startswith('for query,reference in zip'):
        new_source.append("import time\n")
        new_source.append(line)
        new_source.append("    print(f'Processing query: {query}')\n")
        new_source.append("    time.sleep(5)  # Pause to avoid rate limits\n")
    else:
        new_source.append(line)
nb['cells'][1]['source'] = new_source

# Patch Cell 4 (index 4 or the one with evaluate)
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'evaluate(' in "".join(cell.get('source', [])):
        source = cell['source']
        for i, line in enumerate(source):
            if 'max_workers=' in line:
                source[i] = line.replace('max_workers=8', 'max_workers=1')
        cell['source'] = source

with open('eval_try.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

