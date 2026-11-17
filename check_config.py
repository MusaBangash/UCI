import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

print(config["landing"]["folder_id"])
print(config["raw_storage"]["path"])