import json

notebook_path = r"e:\studying\Final Year\ML\Project\VideoSummarizer\task1_(youtube_trans)_local.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

with open("notebook_code.py", "w", encoding="utf-8") as out_f:
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            out_f.write("# %% Code Cell\n")
            out_f.write("".join(cell["source"]))
            out_f.write("\n\n")
