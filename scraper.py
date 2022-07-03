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
    jobs = []
    
    for link in job_links:
        title = get_job_title(link)
        #what_we_look_for_section = get_what_we_look_for_section(link)
        jobs.append(title)
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
        index_seperator = title.find('-')
    except:
        return title
    return title[0:index_seperator+1]

def get_what_we_look_for_section(link: str):
    return "to be implemented"

if __name__ == "__main__":
    #get_job_title("https://be.linkedin.com/jobs/view/consumer-journey-data-analyst-at-philip-morris-international-3149104842?refId=AfPFGtPXU8J%2Fy%2FfwlYYPkA%3D%3D&trackingId=7hxxGdscM3Al1GJjwTVTRg%3D%3D&position=25&pageNum=0&trk=public_jobs_jserp-result_search-card")
    listings = get_listings("Data Analyst", "Belgium")
    findings = analyse_listings(listings)
    print(findings)