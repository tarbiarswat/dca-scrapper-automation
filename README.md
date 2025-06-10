# 🧾 California DCA License Scraper (Certified Public Accountants)

This Python script automates the process of verifying Certified Public Accountant (CPA) licenses on the California Department of Consumer Affairs (DCA) public license portal. It reads a list of names from an Excel file, performs exact-match lookups, filters California-based licenses, logs the outcomes, and exports all results into an Excel spreadsheet with visual highlights.

---

## ✅ Features Summary

- Reads names from an Excel file (`names.xlsx`) starting from **row 4**
- Uses Selenium to search for each name on the [DCA portal](https://search.dca.ca.gov/)
- Filters results to show only:
  - Exact **first name** match
  - Exact **last name** match
  - Only if **State = California**
- Scrolls to load all dynamic results
- Parses full result details using **BeautifulSoup**
- Saves all results (matched or not) in an Excel file
- Adds `"Match Status"` column with either `"Matched"` or `"Not Found"`
- Highlights **matched rows in green**
- Auto-adjusts column widths based on content
- Logs all activity with **timestamped entries** and **record IDs** in `search_log.txt`

---

## 📂 Input Format

Input file: `names.xlsx`  
- Column A: First Name  
- Column B: Last Name  
- Data begins on **row 4**

| First Name | Last Name |
|------------|-----------|
| John       | Smith     |
| David      | Lee       |
| ...        | ...       |

---

## 🛠 Requirements

Install required packages:

```bash
pip install selenium pandas openpyxl beautifulsoup4 webdriver-manager
```

---

## ▶️ How to Run

Run the script:

```bash
python script.py
```

To run in **headless mode** (no browser window), update this in the code:

```python
options.add_argument("--headless=new")
```

---

## 📄 Output Files

**california_matches.xlsx**  
- Contains all looked-up names with detailed info  
- Exact matches marked as `"Matched"`  
- Others as `"Not Found"`  
- Matched rows highlighted in light green  
- Column widths auto-adjusted

**search_log.txt**  
- Logs each record’s result with:
  - Timestamp
  - Record ID
  - Match status or error message

Example log entries:

```
[2025-06-07 13:25:41] Record #0: ✅ Match found for David Lee
[2025-06-07 13:25:45] Record #1: ⛔ Not matched for John Smith
[2025-06-07 13:25:49] No exact match in California for: Jane Doe
```

---

## 📌 Logic Overview

1. Read names from `names.xlsx` (row 4 onward)
2. For each entry:
   - Launch a fresh Chrome browser
   - Search for the full name as a CPA
   - Auto-scroll until no new results load
   - Extract data for each license result
   - Check for exact match and CA state
   - Append to output with `"Matched"` or `"Not Found"`
3. Save all results in `california_matches.xlsx`
4. Log results and issues in `search_log.txt`

---

## 📈 Use Case

- Automate background checks for Certified Public Accountants
- Validate alumni or staff license authenticity
- Reduce manual work in license verification processes

---

## 📤 Reset / Clean Output

To delete output and start over:

```bash
del california_matches.xlsx
del search_log.txt
```

---

## 🧠 Pro Tips

- You can highlight `"Not Found"` rows in red (on request)
- You can export `"Matched"` and `"Not Found"` to separate Excel files
- Script opens a **new browser for each entry** to avoid session conflicts

---

## 📬 Support

If you need customization or run into issues, feel free to reach out.

---
