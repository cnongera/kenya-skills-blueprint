# National Skills Blueprint Generator (Prototype)

## 📌 Project Overview
Developed a pure Python analytical tool to process KNBS/ILO labor market data, calculating a custom 'Vulnerability & Transition Risk Index'. The tool generates automated policy blueprints and M&E trackers, successfully identifying Agriculture and Jua Kali retail as top priorities for foundational digital upskilling, reaching over 4.1 million informal workers.

## 🎯 The Problem
Traditional skills-gap analyses often fail in emerging economies because they rely solely on formal education metrics, ignoring the vast informal sector (e.g., the Jua Kali economy). This tool simulates the analytical work of a Digital & AI Skills Specialist by identifying which sectors are most vulnerable to digital transition and require immediate foundational upskilling.

## ⚙️ Methodology
The script calculates a **Vulnerability Score** for each sector using the formula:
`Vulnerability Score = (100 - Literacy Rate) + Informality Rate + (Demand Growth * 2)`

*   **High Informality:** Sectors with high informal employment (like MSMEs and Agriculture) are harder to reach but require urgent intervention.
*   **Low Literacy:** Identifies where foundational digital skills are needed.
*   **Demand Growth:** Weighs the future urgency of the sector in the digital economy.

## 🚀 Features
*   **Python:** Built entirely with standard libraries (`os`, `csv`, `datetime`). No external frameworks required.
*   **Data Validation:** Cleans and validates raw CSV data (handles percentages, commas, and quotes).
*   **Automated Reporting:** Generates a formatted Markdown (`.md`) policy brief.
*   **M&E Export:** Outputs an Excel-ready (`.csv`) Monitoring & Evaluation tracker with budget estimates and worker targets.

## 🛠️ How to Run
1. Clone this repository.
2. Ensure your `country_data.csv` file is in the same folder as the script. 
3. Run the script:
   python blueprint_generator.py.  
4. Check the output files: Kenya_Skills_Blueprint.md and Kenya_ME_Tracker.csv.


## 📊 Sample Output (Kenya Dataset)
Based on 2024 KNBS/ILO data, the tool automatically identifies the following top priority sectors:

1. Wholesale & Retail Trade (incl. MSMEs): Vulnerability Score 112.2 (4.2M informal workers at risk).
2. Agriculture, Forestry & Fishing: Vulnerability Score 109.2 (4.1M informal workers at risk). 
3. Construction: Vulnerability Score 104.8 (1.2M informal workers at risk). 
