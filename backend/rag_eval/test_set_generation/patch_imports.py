import json

with open('eval_try.ipynb', 'r') as f:
    nb = json.load(f)

# Patch Cell 0 to add missing imports
source = nb['cells'][0]['source']
has_import = False
for line in source:
    if "LLMContextRecall" in line:
        has_import = True
        break

if not has_import:
    source.append("from ragas.metrics import LLMContextRecall, Faithfulness\n")

nb['cells'][0]['source'] = source

with open('eval_try.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

