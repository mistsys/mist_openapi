import yaml

SPEC_FILE = "./openapi.yaml"

with open(SPEC_FILE, "r", encoding="utf-8") as f_in:
    data = yaml.safe_load(f_in)


schemas = data.get("components", {}).get("schemas")
for n, s in schemas.items():
    if s.get("type") == "object":
        for prop, value in s.get("properties", {}).items():
            if value.get("nullable") is True:
                print(f"Setting nullable to OAS3.1 format: {n}.{prop}")
                value["type"] = [value["type"], 'null']
                value.pop("nullable")
            if isinstance(value.get("additionalProperties"), dict):
                additional_props = value["additionalProperties"]
                if additional_props.get("nullable") is True:
                    print(f"Setting nullable to OAS3.1 format: {n}.{prop}.additionalProperties")
                    additional_props["type"] = [additional_props["type"], 'null']
                    additional_props.pop("nullable")
    elif s.get("anyOf") and s.get("nullable") is True:
        s["anyOf"].append({"type": 'null'})
        print(f"Setting nullable to OAS3.1 format: {n}")
        s.pop("nullable")
    elif s.get("oneOf") and s.get("nullable") is True:
        s["oneOf"].append({"type": 'null'})
        print(f"Setting nullable to OAS3.1 format: {n}")
        s.pop("nullable")
    elif s.get("nullable") is True:
            print(f"Setting nullable to OAS3.1 format: {n}")
            s["type"] = [s["type"], 'null']
            s.pop("nullable")
        
data["components"]["schemas"] = schemas

with open(SPEC_FILE, "w", encoding="utf-8") as f:
    yaml.dump({"openapi": data["openapi"]}, f)
    yaml.dump({"info": data["info"]}, f)
    yaml.dump({"servers": data["servers"]}, f)
    yaml.dump({"security": data["security"]}, f)
    yaml.dump({"tags": data["tags"]}, f)
    yaml.dump({"paths": data["paths"]}, f)
    yaml.dump({"components": data["components"]}, f)
