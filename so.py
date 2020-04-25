import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    if pagination:
      last_page = pagination.find_all("a")[-2].get_text(strip=True)
    else:
      return 1
    return int(last_page)

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    if pagination:
      last_page = pagination.find_all("a")[-2].get_text(strip=True)
    else:
      return 1
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {
        "class": "mb4 fc-black-800 fs-body3"
    }).find("a")["title"]
    company, location = html.find( "h3", {
        "class": "mb4"
    }).find_all(
        "span", recursive=False)
    company = company.get_text(strip=True).strip()
    location = location.get_text(strip=True).strip("-")
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    page_one = requests.get(url)
    soup_one = BeautifulSoup(page_one.text, "html.parser")
    no_job = soup_one.find("p", {"class": "ws-pre-wrap"})
    if no_job is not None:
      print("No jobs in StackOverflow")
      return []
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        if last_page > 1:
          result = requests.get(f"{url}&pg={page+1}")
        else:
          result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word, location):
    url = f"https://stackoverflow.com/jobs?q={word}&l={location}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
