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

▶️ How to Run
Run the script: