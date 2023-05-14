import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


base_url = "https://myneta.info"

def generate_tables(table, year, is_winner=True):
    """
    Generate tables based on the data given
    """
    wb = Workbook()
    ws = wb.active
    first_column = ["Sno", "Candidates", "Constituency", "Party", "Criminal case", "Education", "Total Assets", "Liabilities"]
    ws.append(first_column)
    
    rows = table.find_all("tr")
    headings = table.find_all("th")
    
    is_correct_table: bool = False
    is_first_run: bool = True
    is_by_election = False

    for heading in headings:
        if "Candidate" in heading.text.strip():
            is_correct_table = True
            break

    if not is_correct_table:
        return 
       
    for row in rows:
        cols = row.find_all("td")
        if len(cols) <= 1:
            continue
        candidate_col = []
        for col in cols:
            candidate_col.append(col.text.strip())
        if "election" in candidate_col[2].lower() and "bye" in candidate_col[2].lower() and is_first_run:
            is_by_election = True
        is_first_run = False
        ws.append(candidate_col)

    file_name = "Candidates_"
    if is_winner:
        file_name = "Winners_" + file_name

    if is_by_election:
        file_name = file_name + "By_Election_"

    file_name = file_name + year
    print("Done saving the table with name: ", file_name)
    wb.save(file_name + ".xlsx")

        

url = f"{base_url}/state_assembly.php?state=Odisha"
response = requests.get(url)
assert response.status_code == 200
soup = BeautifulSoup(response.content, "html.parser")

"""
Try finding all possible tags that can hold necessary information. Might need to be extended
"""
a_tags = soup.find_all("a")
h_tags = soup.find_all("h")
p_tags = soup.find_all("p")

tags = a_tags + h_tags + p_tags
for tag in tags:
    # Filter all winners but not winners expenses
    if "winners" in tag.text.lower() and "expense" not in tag.text.lower():
        href = tag.get("href")
        year = href.split("/")[1].strip("odisha").strip("orissa")
        
        winner_url = f"{base_url}/{href}"

        winner_response = requests.get(winner_url)
        assert winner_response.status_code == 200
        winner_soup = BeautifulSoup(winner_response.content, "html.parser")
        
        # Find all tables
        tables = winner_soup.find_all("table")
        for table in tables:
            generate_tables(table, year)