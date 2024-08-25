import base64, json


def decode_base64_fix(data):
    fix = "=" * int(len(data) % 4)
    payload = base64.b64decode(data + fix)
    return payload.decode()


def to_json(items):
    output = []
    for item in items:
        tmp = json.loads(item.to_json())
        if "_id" in tmp:
            del tmp["_id"]
        if "objectid" in tmp:
            del tmp["objectid"]
        output.append(tmp)
    return output
