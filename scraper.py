from pandas import array
import requests as req

from bs4 import BeautifulSoup

HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

def get_listings(job_title: str, region: str = "Beglium"):
    """
    Gets the link to all job posts for the given job title & region
    """
    r = req.get(f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={region}", headers=HEADERS)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    job_links = []
    
    for a in soup.find_all('a', href=True):
        if "view" in a['href']:
            job_links.append(a['href'])
    return job_links

def analyse_listings(job_links: array):
    jobs = dict()
    
    for link in job_links:
        title = get_job_title(link)
        required_skills = get_required_skills(link)
        jobs[title] = required_skills
    return jobs

    
def get_job_title(link: str):
    """
    Extracts the job title from the post
    """
    r = req.get(link, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html5lib')
    try:
        title = soup.find("h1").text
    except:
        return f"something went wrong for {link}"
    try:
        return title.split('-')[0]
    except:
        return title

def get_required_skills(link: str):
    return "to be implemented"

if __name__ == "__main__":
    listings = get_listings("Data Analyst", "Belgium")
    findings = analyse_listings(listings)
    print(findings)