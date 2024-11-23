import datetime

# Sample data
report_data = {
    "total_ewaste_collected": 5000,  # kg
    "total_recycled": 4500,  # kg
    "total_disposed": 500,  # kg
    "annual_compliance_target": 4800,  # kg
    "total_co2_reduced": 1200,  # kg
    "collection_centers": {
        "Center A": {"collected": 2000, "recycled": 1800, "disposed": 200},
        "Center B": {"collected": 1500, "recycled": 1300, "disposed": 200},
        "Center C": {"collected": 1500, "recycled": 1400, "disposed": 100},
    },
    "financials": {
        "total_costs": 10000,  # Currency unit
        "savings_from_recycling": 2500,  # Currency unit
        "revenue_from_resold_items": 1500,  # Currency unit
    },
}

# Function to generate report
def generate_compliance_report(data):
    report_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # 1. Executive Summary
    print(f"Compliance Report - E-Waste Management\nDate: {report_date}")
    print("\n--- Executive Summary ---")
    total_ewaste_collected = data["total_ewaste_collected"]
    total_recycled = data["total_recycled"]
    total_disposed = data["total_disposed"]
    compliance_percentage = (total_recycled / data["annual_compliance_target"]) * 100
    print(f"Total E-Waste Collected: {total_ewaste_collected} kg")
    print(f"Total E-Waste Recycled: {total_recycled} kg")
    print(f"Total E-Waste Disposed: {total_disposed} kg")
    print(f"Compliance with Annual Target: {compliance_percentage:.2f}%\n")

    # 2. Detailed Metrics
    print("--- Key Metrics ---")
    print(f"CO₂ Reduction from Recycling: {data['total_co2_reduced']} kg")
    print(f"Compliance Target for the Year: {data['annual_compliance_target']} kg")
    print(f"Compliance Rate: {compliance_percentage:.2f}%")
    if compliance_percentage >= 100:
        print("Status: Target met or exceeded")
    else:
        print("Status: Below target, further action needed")

    # 3. Financial Analysis
    print("\n--- Financial Analysis ---")
    total_costs = data["financials"]["total_costs"]
    savings_from_recycling = data["financials"]["savings_from_recycling"]
    revenue_from_resold_items = data["financials"]["revenue_from_resold_items"]
    net_savings = savings_from_recycling + revenue_from_resold_items - total_costs
    print(f"Total Costs: {total_costs}")
    print(f"Savings from Recycling: {savings_from_recycling}")
    print(f"Revenue from Resold Items: {revenue_from_resold_items}")
    print(f"Net Savings: {net_savings} (after recycling and resale)\n")

    # 4. Geographic Insights - Collection Centers Performance
    print("--- Geographic Insights: Collection Centers ---")
    for center, stats in data["collection_centers"].items():
        collected = stats["collected"]
        recycled = stats["recycled"]
        disposed = stats["disposed"]
        recycling_rate = (recycled / collected) * 100
        print(f"{center} - Collected: {collected} kg, Recycled: {recycled} kg ({recycling_rate:.2f}%), Disposed: {disposed} kg")

    # 5. Improvement Recommendations
    print("\n--- Improvement Recommendations ---")
    if compliance_percentage < 100:
        print("1. Increase recycling capacity at underperforming centers.")
        print("2. Launch awareness programs to improve collection rates.")
        print("3. Consider partnerships with third-party recyclers to enhance efficiency.")
    else:
        print("Compliance targets met. Focus on maintaining and scaling current efforts.")

    # 6. Historical Trends and Projections (Placeholder for Visualization)
    print("\n--- Historical Trends and Projections ---")
    print("Data Visualization Placeholder: Add monthly and yearly trend charts showing e-waste collection and recycling rates.")

    # 7. Customer/Community Feedback Section
    print("\n--- Community Feedback ---")
    print("Placeholder: Include summary of public feedback on recycling programs and any suggestions for improvement.")

    # 8. Compliance by Regulation
    print("\n--- Compliance by Regulation ---")
    print("Placeholder: List specific environmental regulations (e.g., WEEE compliance) and indicate compliance status.")
    
    # 9. Appendix - Glossary
    print("\n--- Appendix ---")
    print("Glossary: Definitions of terms related to e-waste and compliance management.")

# Generate the report
generate_compliance_report(report_data)
