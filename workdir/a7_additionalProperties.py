import yaml

SPEC_FILE = "./openapi.yaml"
EXCEPTIONS = []

with open(SPEC_FILE, "r") as f_in:
    data = yaml.load(f_in, Loader=yaml.loader.SafeLoader)

path = data.get("paths", {})
for p, v in path.items():
    for m, o in v.items():
        if isinstance(o, dict) is False:
            continue
        schema = o.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {}).get("$ref")
        if schema:
            ref_name = schema.split("/")[-1]
            if ref_name not in EXCEPTIONS:
                # print(f"Adding exception for {ref_name} from requestBody in {p} {m}")
                EXCEPTIONS.append(ref_name)



schemas = data.get("components", {}).get("schemas")
for n, s in schemas.items():
    if n not in EXCEPTIONS and s.get("additionalProperties") is None and s.get("type") == "object":
        print(f"Setting additionalProperties to False for schema: {n}")
        s["additionalProperties"] = False
        
data["components"]["schemas"] = schemas

with open(SPEC_FILE, "w") as f:
    yaml.dump(data, f, sort_keys=False)
