import csv
import json
import urllib.request

# Replace this with your Google Sheet export link (CSV format)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSKT85C6cZdhhjob-pnRUk6HvSLjZVK3yizUiB_Qb0kuYDt883Z6m5Oc3LL1lLlTNwP_fIkwFnQ2DyK/pub?output=csv"

with urllib.request.urlopen(CSV_URL) as response:
    lines = [l.decode('utf-8') for l in response.readlines()]
    reader = csv.DictReader(lines)

    features = []
    for row in reader:
        try:
            coords = json.loads(row["geometry"])
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": coords
                },
                "properties": {
                    "field_officer": row.get("field_officer", ""),
                    "area_name": row.get("area_name", ""),
                    "photo_url": row.get("photo_url", "")
                }
            }
            features.append(feature)
        except Exception as e:
            print("Error processing row:", e)
            continue

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open("data.geojson", "w") as f:
        json.dump(geojson, f, indent=2)
