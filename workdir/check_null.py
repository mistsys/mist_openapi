import yaml

SPEC_FILE = "./openapi.yaml"

with open(SPEC_FILE, "r", encoding="utf-8") as f_in:
    data = yaml.safe_load(f_in)


schemas = data.get("components", {}).get("schemas")
for schema_name, schema in schemas.items():
    if schema.get("type") == "object":
        for prop, value in schema.get("properties", {}).items():
            if value.get("nullable") is True:
                print(f"Setting nullable to OAS3.1 format: {schema_name}.{prop}")
                value["type"] = [value["type"], 'null']
                value.pop("nullable")
            if isinstance(value.get("additionalProperties"), dict):
                additional_props = value["additionalProperties"]
                if additional_props.get("nullable") is True:
                    print(f"Setting nullable to OAS3.1 format: {schema_name}.{prop}.additionalProperties")
                    additional_props["type"] = [additional_props["type"], 'null']
                    additional_props.pop("nullable")
    elif schema.get("anyOf") and schema.get("nullable") is True:
        schema["anyOf"].append({"type": "null"})
        print(f"Setting nullable to OAS3.1 format: {schema_name}")
        schema.pop("nullable")
    elif schema.get("oneOf") and schema.get("nullable") is True:
        schema["oneOf"].append({"type": "null"})
        print(f"Setting nullable to OAS3.1 format: {schema_name}")
        schema.pop("nullable")
    elif schema.get("nullable") is True:
            print(f"Setting nullable to OAS3.1 format: {schema_name}")
            schema["type"] = [schema["type"], "null"]
            schema.pop("nullable")
data["components"]["schemas"] = schemas

with open(SPEC_FILE, "w", encoding="utf-8") as f:
    yaml.dump(data, f, sort_keys=False)
