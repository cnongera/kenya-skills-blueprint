# =============================================================================
#  NATIONAL SKILLS BLUEPRINT & PERSONAL DIAGNOSTIC SIMULATOR (v4.1)
# -----------------------------------------------------------------------------
# PURPOSE:
#   Simulates the core deliverable of a Digital & AI Skills
#   Specialist: turning a country's raw skills data into a
#   structured, policy-ready "National Skills Blueprint".
# 
#  This script combines MACRO-level policy design (national skills blueprint)
#  with MICRO-level individual assessment (competency framework & pathway).
#  
#  It directly mirrors four duty clusters:
#     1. Develop BLUEPRINTS, TOOLKITS and DIAGNOSTICS for digital user skills
#     2. Link digital skills investments to REAL EMPLOYMENT OUTCOMES
#     3. Design national AI skills strategies, COMPETENCY FRAMEWORKS and
#        LEARNING PATHWAYS
#     4. Support PARTNERSHIPS (by providing transparent, honest modeling)
#
#  DESIGN CONSTRAINTS:
#   - Pure Python only (standard library: os, csv, random, datetime).
#   - No frameworks, no functions, no classes. Straight linear execution.
#   - Heavily commented for transparency.
# =============================================================================

import os
import csv
import datetime
import random

# =============================================================================
# PART 1: MACRO-LEVEL CONFIGURATION & DATA INGESTION
# =============================================================================
COUNTRY_NAME   = "Republic of Kenya"
VULNERABILITY_THRESHOLD = 90
TARGET_YEARS   = 3                        
COST_PER_WORKER = 35            
REPORT_PATH_TXT = "Kenya_Skills_Blueprint.txt"
REPORT_PATH_MD  = "Kenya_Skills_Blueprint.md"
REPORT_PATH_CSV = "Kenya_ME_Tracker.csv"

sector_data = []   

# Load the CSV data
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
    print("Error: country_data.csv not found. Please create it first.")
    exit()

# =============================================================================
# PART 2: MACRO-LEVEL CALCULATIONS (Vulnerability Index)
# =============================================================================
for s in sector_data:
    # Calculate Vulnerability Score
    s["vulnerability"] = round((100.0 - s["literacy"]) + s["informal"] + (s["demand_growth"] * 2), 1)
    s["priority"] = "YES" if s["vulnerability"] >= VULNERABILITY_THRESHOLD else "no"
    s["total_workers"] = int(s["workforce_k"] * 1000)
    s["informal_workers"] = int(s["total_workers"] * (s["informal"] / 100))
    s["workers_to_upskill"] = int(s["total_workers"] * ((100.0 - s["literacy"]) / 100))
    s["estimated_budget"] = s["workers_to_upskill"] * COST_PER_WORKER

    if s["literacy"] < 80.0:
        s["pathway"] = "Foundational Digital Literacy & Mobile Money Skills"
    elif s["literacy"] < 95.0:
        s["pathway"] = "Productivity Tools, Cloud Basics & E-commerce"
    else:
        s["pathway"] = "Advanced Data Science, AI Prompting & Cybersecurity"

# =============================================================================
# PART 3: MACRO-LEVEL REPORT GENERATION (Text, Markdown, CSV)
# =============================================================================
lines = []                       
year_now = datetime.date.today().year
target_year = year_now + TARGET_YEARS
divider = "=" * 80
subdivider = "-" * 80

lines.append(divider)
lines.append("NATIONAL DIGITAL & AI SKILLS BLUEPRINT")
lines.append("Country        : " + COUNTRY_NAME)
lines.append("Generated      : " + str(datetime.date.today()))
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

with open(REPORT_PATH_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

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

with open(REPORT_PATH_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

with open(REPORT_PATH_CSV, "w", encoding="utf-8") as f:
    f.write("Sector,Vulnerability_Score,Informal_Workers,Workers_Targeted,Budget_USD\n")
    for s in sector_data:
        if s["priority"] == "YES":
            f.write(s["sector"] + "," + str(s["vulnerability"]) + "," + str(s["informal_workers"]) + "," + str(s["workers_to_upskill"]) + "," + str(s["estimated_budget"]) + "\n")

print("MACRO-LEVEL BLUEPRINT GENERATED.")
print("Files saved: " + REPORT_PATH_MD + ", " + REPORT_PATH_CSV)
print("\n")

# =============================================================================
# PART 4: MICRO-LEVEL DIAGNOSTIC (Competency Framework & Individual Pathway)
# =============================================================================
print("=" * 80)
print("  AI SKILLS DIAGNOSTIC & PATHWAY SIMULATOR (Individual Assessment)")
print("=" * 80)
print("Now, let's assess an individual's readiness for the AI economy.")
print("You will answer 12 short questions.\n")

# --- Intake ---
user_name = ""
while user_name.strip() == "":
    user_name = input("Your name (for the report): ").strip()

print("\nWhich sector do you work in?")
for idx, s in enumerate(sector_data, start=1):
    print("  " + str(idx) + " = " + s["sector"])
sector_choice = ""
while not sector_choice.isdigit() or int(sector_choice) < 1 or int(sector_choice) > len(sector_data):
    sector_choice = input("Choose 1-" + str(len(sector_data)) + ": ").strip()
user_sector = sector_data[int(sector_choice) - 1]["sector"]

print("\nHighest education level completed:")
print("  1 = Secondary          2 = Vocational / TVET")
print("  3 = Bachelor's         4 = Master's or higher")
edu_map = {"1": "Secondary", "2": "Vocational/TVET", "3": "Bachelor's", "4": "Master's+"}
edu_choice = ""
while edu_choice not in edu_map:
    edu_choice = input("Choose 1-4: ").strip()
    if edu_choice not in edu_map:
        print("  -> Please type a number from 1 to 4.")
user_education = edu_map[edu_choice]

BASELINE_EMPLOYMENT = {
    "Secondary":       0.45,
    "Vocational/TVET": 0.58,
    "Bachelor's":      0.68,
    "Master's+":       0.75,
}

# --- The Diagnostic Engine ---
FRAMEWORK_NAME = "Mini AI User Competency Framework v1.0 (4 domains)"
DOMAIN_NAMES = [
    "AI Foundations & Data Fluency",
    "Prompting & AI Tool Use",
    "Responsible AI & Ethics",
    "Applied Problem-Solving",
]
DOMAIN_CODES = ["A", "B", "C", "D"]

DIAGNOSTIC_ITEMS = [
    (0, "I can explain what machine learning is, and what it is NOT, to a colleague."),
    (0, "I can read a simple table or chart of data and spot an obvious problem in it."),
    (0, "I understand why the quality of training data changes the quality of an AI tool."),
    (1, "I use an AI assistant (e.g. a chatbot) for real tasks at work at least weekly."),
    (1, "I write step-by-step prompts with context, role and required output format."),
    (1, "I always verify AI output against a reliable source before using it."),
    (2, "I can name two risks of AI systems (e.g. bias, privacy) and how they arise."),
    (2, "I know what personal data must never be pasted into a public AI tool."),
    (2, "I can explain to a junior colleague when NOT to trust an AI answer."),
    (3, "I have used AI to complete a concrete work product end-to-end in the last month."),
    (3, "I can estimate how AI would change the tasks in my own occupation."),
    (3, "I have taught or shown at least one other person how to use an AI tool well."),
]

# --- EXPLANATORY SCALE LEGEND ---
print("\n" + "-" * 74)
print("SCALE EXPLANATION - Please use the following ratings:")
print("  1 = Never done it / No understanding")
print("  2 = Heard of it / Vaguely familiar")
print("  3 = Tried it / Basic understanding")
print("  4 = Do it regularly / Confident")
print("  5 = Could teach it to others / Expert")
print("-" * 74 + "\n")

answers = []
for i, (domain_idx, question) in enumerate(DIAGNOSTIC_ITEMS, start=1):
    print("Q%02d. [%s] %s" % (i, DOMAIN_CODES[domain_idx], question))
    raw = ""
    while raw not in ("1", "2", "3", "4", "5"):
        # Added a quick reminder of the scale directly in the input prompt
        raw = input("     Your answer (1=Never, 2=Heard, 3=Tried, 4=Confident, 5=Expert): ").strip()
        if raw not in ("1", "2", "3", "4", "5"):
            print("     -> Please type a single digit from 1 to 5.")
    answers.append(int(raw))
    print()

# --- Score Calculation ---
domain_scores = [0.0, 0.0, 0.0, 0.0]
domain_counts = [0, 0, 0, 0]
for (domain_idx, _question), ans in zip(DIAGNOSTIC_ITEMS, answers):
    domain_scores[domain_idx] += ans
    domain_counts[domain_idx] += 1

for d in range(4):
    avg_on_5 = domain_scores[d] / domain_counts[d]
    domain_scores[d] = round((avg_on_5 - 1) / 4 * 100)

overall_score = round(sum(domain_scores) / 4.0)
overall_level = "Expert"
LEVEL_BANDS = [(40, "Foundation"), (65, "Practitioner"), (85, "Builder"), (101, "Expert")]
for threshold, level_name in LEVEL_BANDS:
    if overall_score < threshold:
        overall_level = level_name
        break

# --- Gap Analysis & Pathway Recommender ---
TARGET_PROFILE = {"A": 75, "B": 70, "C": 70, "D": 65}
gaps = {}

print("\n" + "-" * 74)
print("GAP ANALYSIS vs. 'DIGITAL & AI SKILLS SPECIALIST' BENCHMARK")
print("-" * 74)
print("  %-30s %8s %8s %8s" % ("Domain", "You", "Target", "Gap"))
for d in range(4):
    code = DOMAIN_CODES[d]
    target = TARGET_PROFILE[code]
    gap = target - domain_scores[d]
    gaps[code] = gap
    flag = "  <-- PRIORITY GAP" if gap > 15 else "  (meets target)" if gap <= 0 else ""
    print("  %-30s %8d %8d %8d%s" % (DOMAIN_NAMES[d], domain_scores[d], target, gap, flag))

print("\n" + "-" * 74)
print("RECOMMENDED LEARNING PATHWAY (largest gaps first)")
print("-" * 74)
PATHWAYS = {
    "A": "AI foundations: work through an 'AI for everyone' style open course (4-6 weeks).",
    "B": "AI tool use: complete a prompt-engineering module and apply to 5 real tasks.",
    "C": "Responsible AI: study one national AI-ethics guideline, write a team 'rules of use'.",
    "D": "Applied transfer: redesign ONE work product with AI; document time saved.",
}
order = sorted(range(4), key=lambda d: gaps[DOMAIN_CODES[d]], reverse=True)
step_no = 1
for d in order:
    code = DOMAIN_CODES[d]
    if gaps[code] <= 0:
        print("  Step %d (optional): %s is at target." % (step_no, DOMAIN_NAMES[d]))
    else:
        print("  Step %d [%s - gap %d]: %s" % (step_no, code, gaps[code], PATHWAYS[code]))
    step_no += 1

# =============================================================================
# PART 5: EMPLOYMENT OUTCOMES SIMULATION (Micro-level)
# =============================================================================
print("\n" + "-" * 74)
print("EMPLOYMENT OUTCOMES SIMULATION")
print("-" * 74)

COHORT_SIZE = 1000
random.seed(38713)
UPLIFT_PER_10_POINTS = 0.06
MAX_UPLIFT = 0.35
baseline_prob = BASELINE_EMPLOYMENT[user_education]

before_placed = 0
for _ in range(COHORT_SIZE):
    if random.random() < baseline_prob:
        before_placed += 1

after_placed = 0
skill_scores = []
for _ in range(COHORT_SIZE):
    skill = min(95, max(25, int(random.gauss(55, 15))))
    skill_scores.append(skill)
    uplift = min(MAX_UPLIFT, (skill / 10.0 - 4.0) * UPLIFT_PER_10_POINTS)
    if uplift < 0:
        uplift = 0.0
    p = min(0.95, baseline_prob + uplift)
    if random.random() < p:
        after_placed += 1

before_rate = before_placed / float(COHORT_SIZE) * 100
after_rate = after_placed / float(COHORT_SIZE) * 100
uplift_rate = after_rate - before_rate

print("  Cohort size               : %d simulated learners" % COHORT_SIZE)
print("  Baseline placement (%s)   : %.1f%%" % (user_education, baseline_prob * 100))
print("  Placement BEFORE training : %.1f%%" % before_rate)
print("  Placement AFTER training  : %.1f%%" % after_rate)
print("  Simulated placement uplift: +%.1f percentage points" % uplift_rate)

# =============================================================================
# PART 6: SAVE FINAL COMBINED REPORT
# =============================================================================
date_stamp = datetime.date.today().isoformat()
personal_report_filename = "Personal_Skills_Report_%s_%s.txt" % (user_name.replace(" ", "_"), date_stamp)

with open(personal_report_filename, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("PERSONAL AI SKILLS DIAGNOSTIC REPORT\n")
    f.write("Generated: %s\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    f.write("=" * 80 + "\n\n")
    f.write("Respondent: %s | Sector: %s | Education: %s\n" % (user_name, user_sector, user_education))
    f.write("Overall Proficiency Level: %s (%d/100)\n\n" % (overall_level.upper(), overall_score))
    
    f.write("DOMAIN SCORES:\n")
    for d in range(4):
        f.write("  %s: %d/100 (Target: %d)\n" % (DOMAIN_NAMES[d], domain_scores[d], TARGET_PROFILE[DOMAIN_CODES[d]]))
    
    f.write("\nRECOMMENDED PATHWAY:\n")
    for d in order:
        code = DOMAIN_CODES[d]
        if gaps[code] > 0:
            f.write("  - [%s]: %s\n" % (code, PATHWAYS[code]))
            
    f.write("\nEMPLOYMENT OUTCOMES SIMULATION:\n")
    f.write("  Baseline Placement: %.1f%%\n" % (baseline_prob * 100))
    f.write("  Post-Training Placement: %.1f%%\n" % after_rate)
    f.write("  Uplift: +%.1f percentage points\n" % uplift_rate)

print("\n" + "=" * 80)
print("PERSONAL REPORT SAVED TO: " + personal_report_filename)
print("=" * 80)
