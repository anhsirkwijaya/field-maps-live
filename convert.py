import csv
import json
import urllib.request

# URL to your published Google Sheet as CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSKT85C6cZdhhjob-pnRUk6HvSLjZVK3yizUiB_Qb0kuYDt883Z6m5Oc3LL1lLlTNwP_fIkwFnQ2DyK/pub?output=csv"

# Output file name
OUTPUT_FILE = "data.geojson"

def convert_csv_to_geojson(csv_url, output_file):
    response = urllib.request.urlopen(csv_url)
    lines = [line.decode('utf-8') for line in response.readlines()]
    reader = csv.DictReader(lines)

    features = []

    for row in reader:
        try:
            geometry = json.loads(row["geometry"])  # Convert geometry string to list
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": geometry
                },
                "properties": {
                    "field_officer": row["field_officer"],
                    "area_name": row["area_name"],
                    "photo_url": row["photo_url"]
                }
            }
            features.append(feature)
        except Exception as e:
            print(f"Skipping row due to error: {e}")

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"✅ GeoJSON written to {output_file}")

# Run the function
if __name__ == "__main__":
    convert_csv_to_geojson(CSV_URL, OUTPUT_FILE)
