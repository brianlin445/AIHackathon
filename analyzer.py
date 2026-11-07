import pandas as pd

REQUIRED_COLUMNS = [
    "location",
    "date",
    "ph",
    "dissolved_oxygen",
    "turbidity",
    "temperature"
]


def analyze_water_data(df):

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Make a copy so the original data is unchanged
    df = df.copy()

    # Convert measurements to numeric values
    measurement_columns = [
        "ph",
        "dissolved_oxygen",
        "turbidity",
        "temperature"
    ]

    for col in measurement_columns:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    # Store findings
    results = []

    for _, row in df.iterrows():

        alerts = []

        # Check missing or invalid measurements
        for col in measurement_columns:

            value = row[col]

            if pd.isna(value):
                alerts.append(
                    f"Missing or invalid {col} measurement"
                )

        # Check pH validity and screening range
        ph = row["ph"]

        if pd.notna(ph):

            if not 0 <= ph <= 14:
                alerts.append("Invalid pH measurement")

            elif ph < 6.5 or ph > 8.5:
                alerts.append(
                    "pH outside screening range"
                )

        # Check dissolved oxygen
        oxygen = row["dissolved_oxygen"]

        if pd.notna(oxygen):

            if oxygen < 0:
                alerts.append(
                    "Invalid dissolved oxygen measurement"
                )

            elif oxygen < 5:
                alerts.append(
                    "Low dissolved oxygen reading"
                )

        # Check turbidity
        turbidity = row["turbidity"]

        if pd.notna(turbidity):

            if turbidity < 0:
                alerts.append(
                    "Invalid turbidity measurement"
                )

            elif turbidity > 10:
                alerts.append(
                    "Elevated turbidity reading"
                )

        # Check temperature
        temperature = row["temperature"]

        if pd.notna(temperature) and temperature < 0:
            alerts.append(
                "Invalid temperature measurement"
            )

        # Save results
        results.append({
            "location": row["location"],
            "date": row["date"],
            "ph": ph,
            "dissolved_oxygen": oxygen,
            "turbidity": turbidity,
            "temperature": temperature,
            "alerts": alerts,
            "status": (
                "Review recommended"
                if alerts
                else "No screening alerts"
            )
        })

    return pd.DataFrame(results)
