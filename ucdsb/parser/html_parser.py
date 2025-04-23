import re
from bs4 import BeautifulSoup

def extract_student_id(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    div = soup.find('div', id='student_name_id')
    if div and '-' in div.text:
        name, sid = div.text.strip().split('-', 1)
        return name.strip(), sid.strip()
    return None, None

def extract_term_code(html_content):
    match = re.search(r'"TERM_CODE"\s*:\s*"([^"]+)"', html_content)
    if match:
        return match.group(1)
    return "UNKNOWN"
