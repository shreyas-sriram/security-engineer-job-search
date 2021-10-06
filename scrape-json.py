import re
import math
import json
import requests
from bs4 import BeautifulSoup
  
URL = "https://www.glassdoor.co.in/Interview/us-security-engineer-interview-questions-SRCH_IL.0,2_IN1_KO3,20_SDRD_IP{}.htm"
headers = {
    'User-Agent': 'Mozilla/5.0'
}

_count = 1

def find_total_pages():
    url = URL.format(1)
    data = requests.get(url, headers=headers).text

    total_questions = re.findall("totalSearchResults.*,\n",data)[0]
    total_questions = re.findall('[0-9]+',total_questions)[0]
    print("Total questions: {}".format(total_questions))

    total_pages = math.ceil(int(total_questions) / 10)
    print("Total pages: {}".format(total_pages))

    return total_pages

def parse_page(wrapper):
    page_data = []

    for data in wrapper:
        parsed_data = parse_data(data)
        page_data.append(parsed_data)
        print("Parsed page\n")

    return page_data

def parse_data(data):
    global _count
    parsed_data = {}

    # job position
    job_position = data.find("span", class_="authorInfo")
    _cleaned_text = job_position.get_text().replace(" was asked...","")
    _position, _company = _cleaned_text.split(" at ")
    # print(_position, _company)

    # job date
    job_date = data.find("div", class_="cell alignRt noWrap minor hideHH")
    _date = job_date.get_text().strip()
    # print(_date)

    # question
    question = data.find("p", class_="questionText")
    # print(question)
    # print(question.get_text())
    _question = question.get_text().strip()
    # print(_question)

    # answers
    _answer = []
    answers = data.find_all("p", class_="noMargVert")
    # if len(answers) == 0:
    #     _answer.append("No answers")
    
    for answer in answers:
        _answer.append(answer.get_text())
        
    # print(_answer)

    parsed_data['key'] = _count
    parsed_data['position'] = _position
    parsed_data['company'] = _company
    parsed_data['date'] = _date
    parsed_data['question'] = _question
    parsed_data['answer'] = _answer

    _count += 1

    print("Parsed data: \n{}".format(json.dumps(parsed_data)))

    return parsed_data

# program control begins here
total_pages = find_total_pages()
print("Total pages: {}".format(total_pages))

all_data = []

for page_number in range(total_pages):
    print("Parsing page: {}\n".format(page_number + 1))

    url = URL.format(page_number + 1)
    data = requests.get(url, headers=headers).text

    soup = BeautifulSoup(data, "html.parser")
    
    wrapper = soup.find_all("div", class_="interviewQuestionWrapper")
    page_data = parse_page(wrapper)

    all_data.extend(page_data)


f = open("questions.json", "w")
f.write(json.dumps(all_data))
print("Data written to file\n")
f.close()
