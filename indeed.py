import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    if pagination:
      links = pagination.find_all("a")
    else: 
      return 1
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company is not None:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string).strip()
        else:
            company = str(company.string).strip()
    else:
        company = "No Company name"
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://au.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page, url, limit):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page}")
        if last_page > 1:
          result = requests.get(f"{url}&start={page*limit}")
        else:
          result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word, location):
    limit = 50
    url = f"https://au.indeed.com/jobs?q={word}&l={location}&limit={limit}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url, limit)
    return jobs