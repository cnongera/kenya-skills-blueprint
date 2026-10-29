# ==============================================================
# NATIONAL SKILLS BLUEPRINT GENERATOR  (Prototype v3.0 - Kenya)
# --------------------------------------------------------------
# # PURPOSE:
#   Simulates the core deliverable of a Digital & AI Skills
#   Specialist: turning a country's raw skills data into a
#   structured, policy-ready "National Skills Blueprint".
# 
# UPDATED LOGIC:
#   - Changed "Gap" to "Vulnerability Score" to accurately 
#     reflect the Kenya dataset.
#   - Added "Informal Workers at Risk" metric.
# ==============================================================

import os
import csv
import datetime

# --------------------------------------------------------------
# STEP 1 - CONFIGURATION
# --------------------------------------------------------------
COUNTRY_NAME   = "Republic of Kenya"
VULNERABILITY_THRESHOLD = 90    # Sectors scoring above this are PRIORITY
TARGET_YEARS   = 3                        
COST_PER_WORKER = 35            # Cost in USD to upskill one worker
REPORT_PATH_TXT = "Kenya_Skills_Blueprint.txt"
REPORT_PATH_MD  = "Kenya_Skills_Blueprint.md"
REPORT_PATH_CSV = "Kenya_ME_Tracker.csv"

# --------------------------------------------------------------
# STEP 2 - DATA INPUT
# --------------------------------------------------------------
sector_data = []   

if os.path.exists("country_data.csv"):
    with open("country_data.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            clean_literacy = row["literacy"].replace("%", "").strip()
            clean_demand = row["demand_growth"].replace("%", "").strip()
            clean_informal = row["informal"].replace("%", "").strip()
            clean_workforce = row["workforce_k"].replace(",", "").replace('"', '').strip()

            sector_data.append({
                "sector":        row["sector"],
                "literacy":      float(clean_literacy),
                "demand_growth": float(clean_demand),
                "informal":      float(clean_informal),
                "workforce_k":   float(clean_workforce),
            })
else:
    print("Error: country_data.csv not found.")
    exit()

# --------------------------------------------------------------
# STEP 3 - CALCULATIONS
# --------------------------------------------------------------
for s in sector_data:
    # NEW LOGIC: Vulnerability Score (0 to 250 scale)
    # We weight demand growth x2 because it represents future urgency.
    s["vulnerability"] = round((100.0 - s["literacy"]) + s["informal"] + (s["demand_growth"] * 2), 1)
    
    # Flag as priority if vulnerability is high
    s["priority"] = "YES" if s["vulnerability"] >= VULNERABILITY_THRESHOLD else "no"

    # Estimate total workforce in absolute numbers
    s["total_workers"] = int(s["workforce_k"] * 1000)
    
    # Estimate Informal Workers (who are hardest to reach)
    s["informal_workers"] = int(s["total_workers"] * (s["informal"] / 100))
    
    # Estimate workers needing training based on lack of literacy
    s["workers_to_upskill"] = int(s["total_workers"] * ((100.0 - s["literacy"]) / 100))
    
    # Budget estimation
    s["estimated_budget"] = s["workers_to_upskill"] * COST_PER_WORKER

    # Pathway logic
    if s["literacy"] < 80.0:
        s["pathway"] = "Foundational Digital Literacy & Mobile Money Skills"
    elif s["literacy"] < 95.0:
        s["pathway"] = "Productivity Tools, Cloud Basics & E-commerce"
    else:
        s["pathway"] = "Advanced Data Science, AI Prompting & Cybersecurity"

# --------------------------------------------------------------
# STEP 4 - BUILD THE TEXT REPORT
# --------------------------------------------------------------
lines = []                       
year_now = datetime.date.today().year
target_year = year_now + TARGET_YEARS
divider = "=" * 80
subdivider = "-" * 80

lines.append(divider)
lines.append("NATIONAL DIGITAL & AI SKILLS BLUEPRINT")
lines.append("Country        : " + COUNTRY_NAME)
lines.append("Generated      : " + str(datetime.date.today()))
lines.append("Methodology    : Vulnerability & Transition Risk Index")
lines.append(divider)
lines.append("")

lines.append("SECTION 1 - SECTOR VULNERABILITY SUMMARY")
lines.append(subdivider)
lines.append("Sector".ljust(30) + "Lit %".rjust(8) + "Informal %".rjust(12) + "Vuln Score".rjust(12) + "Priority".rjust(10))
lines.append("-" * 80)

for s in sector_data:
    lines.append(
        s["sector"][:28].ljust(30) +
        str(s["literacy"]).rjust(8) +
        str(s["informal"]).rjust(12) +
        str(s["vulnerability"]).rjust(12) +
        s["priority"].rjust(10)
    )
lines.append("")

lines.append("SECTION 2 - PRIORITY SECTORS (Vulnerability >= 90)")
lines.append(subdivider)
priority_count = 0    
for s in sector_data:
    if s["priority"] == "YES":
        priority_count += 1
        lines.append("")
        lines.append(str(priority_count) + ". " + s["sector"].upper())
        lines.append("   Vulnerability Score   : " + str(s["vulnerability"]))
        lines.append("   Total Workforce       : " + format(s["total_workers"], ","))
        lines.append("   Informal Workers      : " + format(s["informal_workers"], ",") + " (Hardest to reach)")
        lines.append("   Workers to Upskill    : " + format(s["workers_to_upskill"], ","))
        lines.append("   Estimated Budget      : $" + format(s["estimated_budget"], ","))
        lines.append("   Proposed Pathway      : " + s["pathway"])

lines.append("")
lines.append("Total priority sectors: " + str(priority_count) + " of " + str(len(sector_data)))
lines.append("")

with open(REPORT_PATH_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# --------------------------------------------------------------
# STEP 5 - BUILD THE MARKDOWN REPORT
# --------------------------------------------------------------
md = []
md.append("# National Digital & AI Skills Blueprint: " + COUNTRY_NAME)
md.append("**Generated:** " + str(datetime.date.today()))
md.append("")
md.append("## 1. Sector Vulnerability Summary")
md.append("| Sector | Literacy | Informality | Vulnerability Score | Priority |")
md.append("| :--- | :--- | :--- | :--- | :--- |")

for s in sector_data:
    md.append("| " + s["sector"] + " | " + str(s["literacy"]) + "% | " + str(s["informal"]) + "% | " + str(s["vulnerability"]) + " | **" + s["priority"] + "** |")

md.append("")
md.append("## 2. Priority Actions & Budget")
for s in sector_data:
    if s["priority"] == "YES":
        md.append("### " + s["sector"])
        md.append("* **Informal Workers at Risk:** " + format(s["informal_workers"], ","))
        md.append("* **Target for Upskilling:** " + format(s["workers_to_upskill"], ",") + " workers")
        md.append("* **Budget Estimate:** $" + format(s["estimated_budget"], ","))
        md.append("* **Learning Pathway:** " + s["pathway"])
        md.append("")

with open(REPORT_PATH_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# --------------------------------------------------------------
# STEP 6 - EXPORT M&E TRACKER
# --------------------------------------------------------------
with open(REPORT_PATH_CSV, "w", encoding="utf-8") as f:
    f.write("Sector,Vulnerability_Score,Informal_Workers,Workers_Targeted,Budget_USD\n")
    for s in sector_data:
        if s["priority"] == "YES":
            f.write(s["sector"] + "," + str(s["vulnerability"]) + "," + str(s["informal_workers"]) + "," + str(s["workers_to_upskill"]) + "," + str(s["estimated_budget"]) + "\n")

# --------------------------------------------------------------
# STEP 7 - CONSOLE SUMMARY
# --------------------------------------------------------------
print("==========================================================================")
print("KENYA BLUEPRINT GENERATED SUCCESSFULLY (v3.0)")
print("==========================================================================")
print("Sectors scored : " + str(len(sector_data)))
print("Priority count : " + str(priority_count))
print("--------------------------------------------------------------------------")
print("FILES CREATED:")
print("1. " + REPORT_PATH_TXT)
print("2. " + REPORT_PATH_MD  + " (Open this to see the beautiful tables!)")
print("3. " + REPORT_PATH_CSV + " (Open in Excel)")
print("==========================================================================")