from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from collections import defaultdict
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load and preprocess the dataset
df = pd.read_csv("GTD-suicide.csv", encoding="ISO-8859-1")
print(df.columns)  # This will print all the column names

# Replace -99 with NaN for before aggregation
df["nperps"] = pd.to_numeric(df["nperps"], errors="coerce")
df.replace(-99, np.nan, inplace=True)
df.replace("Unknown", np.nan, inplace=True)


df.dropna(subset=["region_txt", "country_txt", "city"], inplace=True)


# Fill missing date values with default values
df["iyear"].fillna(0, inplace=True)
df["imonth"].fillna(0, inplace=True)
df["iday"].fillna(0, inplace=True)
df["iday"] = df["iday"].replace(0, 1)  # Replace 0th day with 1st

# Convert year, month, day to a datetime object
df["date"] = pd.to_datetime(
    {
        "year": df["iyear"],
        "month": df["imonth"].clip(lower=1),
        "day": df["iday"].replace(0, 1),
    },
    errors="coerce",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/timeline_data", methods=["POST"])
def timeline_data():
    try:
        filters = request.json.get("filters", {})

        # Assuming df is your DataFrame loaded with the necessary data
        filtered_data = (
            df.copy()
        )  # Create a copy of the dataframe to avoid modifying the original

        # Example of filtering logic based on received filters (adjust as necessary)
        if filters.get("date_range"):
            start_date, end_date = filters["date_range"]
            filtered_data = filtered_data[
                (filtered_data["date"] >= start_date)
                & (filtered_data["date"] <= end_date)
            ]

        # Generating timeline data
        # Adjust this example aggregation to fit your dataset and requirements
        timeline_data = (
            filtered_data.groupby(
                [filtered_data["date"].dt.year, filtered_data["date"].dt.month]
            )
            .agg(
                event_count=("eventid", "size"),
                date_min=("date", "min"),
                date_max=("date", "max"),
            )
            .rename_axis(["year", "month"])
            .reset_index()
        )

        # Preparing the response
        timeline_data_dict = timeline_data.to_dict(orient="records")

        return jsonify({"timeline": timeline_data_dict})
    except Exception as e:
        app.logger.error(f"Failed to process timeline data: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["POST"])
def data():
    try:

        bounds = request.json["bounds"]
        zoom_level = request.json["zoom"]

        # Filter points within bounds and exclude unknown coordinates
        visible_points = df[
            (df["latitude"] >= bounds["south"])
            & (df["latitude"] <= bounds["north"])
            & (df["longitude"] >= bounds["west"])
            & (df["longitude"] <= bounds["east"])
            & (df["latitude"].notna())
            & (df["longitude"].notna())
            & (df["city"] != "Unknown")
            & (df["country_txt"] != "Unknown")
            & (df["region_txt"] != "Unknown")
        ]

        # Adjust the grouping criteria based on zoom level
        if zoom_level >= 6:
            # If zoomed in to city level, group by region, country, and city
            grouping = ["region_txt", "country_txt", "city"]
        elif zoom_level >= 3:
            # If zoomed in to country level, group by region and country
            grouping = ["region_txt", "country_txt"]
        else:
            # If zoomed out to region level, group only by region
            grouping = ["region_txt"]

        # Group and aggregate data
        grouped = (
            visible_points.groupby(grouping)
            .agg(
                {
                    "latitude": "mean",
                    "longitude": "mean",
                    "nkill": "sum",
                    "nwound": "sum",
                    "nperps": ["mean", "sum"],
                    "eventid": "nunique",
                    "date": ["min", "max"],
                }
            )
            .reset_index()
        )

        # Flatten the MultiIndex for columns (created due to aggregation)
        # Rename columns for JSON serialization
        grouped.columns = [
            "_".join(col).strip() if type(col) is tuple else col
            for col in grouped.columns.values
        ]

        # Correct the column name from 'eventid_count' to 'event_count'
        grouped.rename(columns={"eventid_nunique": "event_count"}, inplace=True)

        # Create a 'date_range' field for the JSON
        grouped["date_range"] = grouped.apply(
            lambda row: f"{row['date_min'].strftime('%Y-%m-%d')} to {row['date_max'].strftime('%Y-%m-%d')}",
            axis=1,
        )

        # Replace NaN and -99 values appropriately
        grouped.replace({np.nan: "Unknown", -99: 0}, inplace=True)

        # Prepare data for JSON response
        result_json = grouped.to_json(orient="records", date_format="iso")

        return jsonify({"points": result_json})

    except KeyError as e:
        app.logger.error(f"KeyError: {e}")
        return jsonify({"error": f"Column(s) {e} do not exist"}), 500
    except Exception as e:
        app.logger.error("Failed to fetch data", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
