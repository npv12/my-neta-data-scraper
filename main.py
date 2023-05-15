import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


base_url = "https://myneta.info"

def generate_tables(table, year, ws, first_column, is_winner=True):
    """
    Generate tables based on the data given
    """
    
    rows = table.find_all("tr")
    headings = table.find_all("th")
    
    is_first_run: bool = True
    is_by_election = False

    heading_text = [heading.text.strip() for heading in headings]
    for col in first_column:
        if col not in heading_text:
            return None
       
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
    print("Done creating the table with name: ", file_name)
    return file_name

        

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
        continue
        href = tag.get("href")
        year = href.split("/")[1].strip("odisha").strip("orissa")
        
        winner_url = f"{base_url}/{href}"

        winner_response = requests.get(winner_url)
        assert winner_response.status_code == 200
        winner_soup = BeautifulSoup(winner_response.content, "html.parser")
        
        # Find all tables
        tables = winner_soup.find_all("table")
        for table in tables:
            wb = Workbook()
            ws = wb.active
            first_column = ["Sno", "Candidates", "Constituency", "Party", "Criminal case", "Education", "Total Assets", "Liabilities"]
            ws.append(first_column)
            file_name = generate_tables(table, year, ws, first_column)
            wb.save(file_name + ".xlsx")
            wb.close()

    elif "all candidates" in tag.text.lower():
        href = tag.get("href")
        year = href.split("/")[1].strip("odisha").strip("orissa")

        candidate_url = f"{base_url}/{href}"

        candidate_response = requests.get(candidate_url)
        assert candidate_response.status_code == 200
        candidate_soup = BeautifulSoup(candidate_response.content, "html.parser")

        h3_tags = candidate_soup.find_all("h3")
        for h3_tag in h3_tags:
            if "list of constituencies" in h3_tag.text.lower():
                table = h3_tag.find_next("table")
                rows = table.find_all("tr")
                wb = Workbook()
                ws = wb.active
                first_column = ["Candidate","Party","Criminal Cases","Education","Age","Total Assets","Liabilities","Constituency"]
                ws.append(first_column)
                for row in rows:
                    cols = row.find_all("td")
                    for col in cols:
                        a_tag = col.find_next("a")

                        if a_tag is None:
                            continue

                        constituency_name = a_tag.text.strip()
                        print("Constituency Name: ", constituency_name)
                        break
                        href = a_tag.get("href")
                        constituency_url = f"{candidate_url}/{href}"
                        constituency_response = requests.get(constituency_url)
                        assert constituency_response.status_code == 200
                        print("Constituency URL: ", constituency_url)
                        
                        constituency_soup = BeautifulSoup(constituency_response.content, "html.parser")
                        tables = constituency_soup.find_all("table")
                        for table in tables:
                            file_name = generate_tables(table, year, ws, first_column, is_winner=False)
                wb.save("All Candidates_" + year + ".xlsx")
                wb.close()