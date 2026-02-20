import json
from datetime import datetime, timezone


# IMPLEMENT: convert ISO timestamp → milliseconds
def iso_to_millis(iso_time: str) -> int:
    dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)


# IMPLEMENT: unify both data formats
def unify_data(data1, data2):
    result = []

    # Format 1 already uses milliseconds
    for item in data1:
        result.append({
            "deviceId": item["deviceId"],
            "timestamp": item["timestamp"],
            "temperature": item["temperature"]
        })

    # Format 2 uses ISO timestamps
    for item in data2:
        result.append({
            "deviceId": item["id"],
            "timestamp": iso_to_millis(item["time"]),
            "temperature": item["temp"]
        })

    return result


def main():
    with open("data-1.json") as f1:
        data1 = json.load(f1)

    with open("data-2.json") as f2:
        data2 = json.load(f2)

    unified = unify_data(data1, data2)

    with open("data-result.json", "w") as out:
        json.dump(unified, out, indent=2)


if __name__ == "__main__":
    main()
