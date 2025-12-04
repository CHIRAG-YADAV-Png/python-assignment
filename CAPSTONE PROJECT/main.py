# main.py
import logging
from pathlib import Path
from analysis import ingest_csv_folder, calculate_daily_totals, calculate_weekly_aggregates, building_wise_summary, find_peak_time, export_csvs
from visualization import create_dashboard
from models import BuildingManager
import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_summary_text(cleaned_df, summary_df, output_dir="output"):
    out = Path(output_dir)
    out.mkdir(exist_ok=True)
    summary_file = out / "summary.txt"

    total_consumption = float(cleaned_df["kWh"].sum()) if not cleaned_df.empty else 0.0
    highest_building = None
    if not summary_df.empty:
        highest_building = summary_df["total_kWh"].idxmax()
        highest_value = float(summary_df["total_kWh"].max())
    else:
        highest_value = 0.0

    peak = find_peak_time(cleaned_df)
    peak_str = "N/A"
    if not peak.empty:
        peak_str = f"{peak['timestamp']} ({peak['kWh']} kWh)"

    daily = calculate_daily_totals(cleaned_df)
    weekly = calculate_weekly_aggregates(cleaned_df)

    with open(summary_file, "w") as f:
        f.write("Campus Energy Summary Report\n")
        f.write("===========================\n\n")
        f.write(f"Report generated: {datetime.datetime.now()}\n\n")
        f.write(f"Total Campus Consumption (all data): {total_consumption:.3f} kWh\n")
        if highest_building:
            f.write(f"Highest Consuming Building: {highest_building} with {highest_value:.3f} kWh (total)\n")
        else:
            f.write("Highest Consuming Building: N/A\n")
        f.write(f"Peak single-reading time: {peak_str}\n\n")
        f.write("Top observations:\n")
        if not daily.empty:
            f.write(f"- Max daily consumption: {daily['daily_kWh'].max():.3f} kWh on {daily['daily_kWh'].idxmax().date()}\n")
        if not weekly.empty:
            f.write(f"- Max weekly consumption: {weekly['weekly_kWh'].max():.3f} kWh (week ending {weekly['weekly_kWh'].idxmax().date()})\n")
        f.write("\nRecommendations:\n")
        f.write("- Investigate highest-consuming buildings for HVAC or equipment inefficiencies.\n")
        f.write("- Consider peak-shaving strategies between 6 PM - 9 PM if peaks occur then.\n")
    logging.info(f"Summary report written to {summary_file}")
    return str(summary_file)

def main():
    logging.info("Starting campus-energy-dashboard pipeline...")

    # 1) Ingest
    cleaned = ingest_csv_folder("data")

    # 2) Aggregations
    daily = calculate_daily_totals(cleaned)
    weekly = calculate_weekly_aggregates(cleaned)
    building_summary = building_wise_summary(cleaned)

    # 3) Export CSVs
    cleaned_path, summary_path = export_csvs(cleaned, building_summary, output_dir="output")
    logging.info(f"Exported cleaned data to {cleaned_path}")
    logging.info(f"Exported building summary to {summary_path}")

    # 4) Visualization
    dashboard_path = create_dashboard(cleaned, output_path="output/dashboard.png")

    # 5) Summary TXT
    summary_txt = generate_summary_text(cleaned, building_summary, output_dir="output")

    logging.info("Pipeline completed successfully.")
    logging.info(f"Outputs in ./output/: {Path('output').iterdir()}")

if __name__ == "__main__":
    main()