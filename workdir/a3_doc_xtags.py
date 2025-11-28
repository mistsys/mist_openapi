""" 
- add x-logo and x-tagGroups to OpenApi Spec
- only required for readocly portal 
"""

import yaml
import json
import re

FILE_IN = "./openapi.yaml"
FILE_OUT_YAML = "../mist.openapi.yaml"
FILE_OUT_JSON = "../mist.openapi.json"
LOGO = {
    "altText": "Juniper-MistAI",
    "backgroundColor": "#FFFFFF",
    "url": "https://www.mist.com/wp-content/uploads/logo.png",
}
GROUPS = [
    {"name": "Admins", "tags": []},
    {"name": "Self","tags": []},
    {"name": "Sites","tags": []},
    {"name": "Orgs","tags": []},
    {"name": "MSPs","tags": []},
    {"name": "Utilities","tags": []},
    {"name": "Installer", "tags": []},
    {"name": "Samples", "tags": []},
    {"name": "Constants","tags": []},
]

PATHS = {}
TAGS = []


def register_tags():
    global GROUPS
    verbs = ["get", "post", "put", "delete"]
    out = {}
    for group in GROUPS:
        out[group["name"]]=[]
    for path, data in PATHS.items():
        for verb, opereration in data.items():
            if verb in verbs:
                tag = opereration["tags"][0]
                cat = tag.split(" ")[0].strip()
                if cat in out:
                    if tag not in out[cat]:
                        if not any(item["name"] == tag for item in TAGS):
                            print(
                                f"[INFO] Missing tag definition: '{tag}' (path='{path}', verb='{verb}', cat='{cat}')"
                            )
                        out[cat].append(tag)
                else:
                    print(f"Missing tag group for {tag}")
    for group in GROUPS:
        out[group["name"]].sort()
        group["tags"]= out[group["name"]]

    # check for unused tag
    for tag in TAGS:
        used = False
        for group in GROUPS:
            if tag["name"] in group["tags"]:
                used = True
        if not used:
            print(f"UNUSED TAG: {tag}")
        

with open(FILE_IN, "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths", {})
    TAGS = data.get("tags", [])

register_tags()
data["info"]["x-logo"] = LOGO

### update links
data_str = json.dumps(data, indent=4, default=str)
LINK_RE = r"\$e/[^^/]*/"
data_str=re.sub(LINK_RE, "/#operations/", data_str)
data = json.loads(data_str)

with open(FILE_OUT_YAML, "w", encoding="utf-8") as f:
    yaml.dump(data, f, sort_keys=False)


with open(FILE_OUT_JSON, "w", encoding="utf-8") as oas_out_file:
    json.dump(data, oas_out_file)
