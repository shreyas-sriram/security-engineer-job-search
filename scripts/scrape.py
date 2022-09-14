"""
    ### Security Engineer, Salesforce
    ---
    > 11 Jan 2021
    <details><summary>Question</summary>
    <p>

    - answer 1
    - answer 2

    </p>
    </details>
"""

import re
import math
import requests
from bs4 import BeautifulSoup

# api-endpoint
URL = "https://www.glassdoor.co.in/Interview/us-security-engineer-interview-questions-SRCH_IL.0,2_IN1_KO3,20_SDRD_IP{}.htm"
headers = {
    'User-Agent': 'Mozilla/5.0'
}


def find_total_pages():
    # sending get request and saving the response as response object
    url = URL.format(1)
    data = requests.get(url, headers=headers).text

    # calculate total pages
    total_questions = re.findall("totalSearchResults.*,\n", data)[0]
    total_questions = re.findall('[0-9]+', total_questions)[0]
    print("Total questions: {}".format(total_questions))

    total_pages = math.ceil(int(total_questions) / 10)
    print("Total pages: {}".format(total_pages))

    return total_pages


def parse_page(wrapper):
    f = open("./questions/questions.md", "a")

    for data in wrapper:
        parsed_data = parse_data(data)
        f.write(parsed_data)
        print("Data written to file\n")

    f.close()
    return


def parse_data(data):
    parsed_data = ""

    # job position
    job_position = data.find("a", class_="css-1mig9hw edupdmz4")
    _cleaned_text = job_position.get_text().replace(" was asked...", "")
    parsed_data = parsed_data + "## {}".format(_cleaned_text)
    # print(job_position.get_text())

    # company
    company = data.find("img", class_="css-1yo1500 edupdmz0")
    if company:
        parsed_data = parsed_data + ", {}".format(company['alt'])
    # print(company['alt'])

    parsed_data = parsed_data + "\n"

    # job date
    job_date = data.findAll("span", class_="m-0 css-1jlgt0v edupdmz5")[1]
    _cleaned_text = job_date.get_text().strip()
    parsed_data = parsed_data + "> {}".format(_cleaned_text)
    # print(job_date.get_text())

    parsed_data = parsed_data + "\n\n"

    # question
    question = data.find("h3", class_="css-11euy82 edupdmz3")
    # print(question)
    # print(question.get_text())
    _cleaned_text = question.get_text().strip()

    answers = data.find_all("span", class_=None)
    if len(answers) == 0:
        parsed_data = parsed_data + _cleaned_text
    else:
        parsed_data = parsed_data + \
            "<details><summary>{}</summary>".format(_cleaned_text)
        # print(question.get_text())

        parsed_data = parsed_data + "\n<p>\n\n"

        for answer in answers:
            answer = answer.get_text().replace(" Less", "")
            parsed_data = parsed_data + "- {}\n".format(answer)
            # print(answer)

        parsed_data = parsed_data + "\n</p>\n</details>"

    parsed_data = parsed_data + "\n\n"

    print("Parsed data: \n{}".format(parsed_data))

    return parsed_data


# program control begins here
total_pages = find_total_pages()
print("Total pages: {}".format(total_pages))

for page_number in range(total_pages):
    print("Parsing page: {}\n".format(page_number + 1))

    url = URL.format(page_number + 1)
    data = requests.get(url, headers=headers).text

    soup = BeautifulSoup(data, "html.parser")

    wrapper = soup.find_all("div", class_="col d-flex")
    parse_page(wrapper)
