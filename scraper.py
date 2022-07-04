import re 
import pandas as pd
import requests as req

from pandas import array
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
SKILLS = 'Master|Bachelor|SQL|Python|SAS|Pyspark|AWS|GCP|Google|Amazon|Azure|Excel|Power|Tableau|QlikView|Hadoop|Spark|docker|kubernetes|Oracle|Pandas|Dash|Scikit|TensorFlow|Keras|git|Airflow|Java|Golang|warehouse|lake|Modeling|Linux|Cloudera|HDFS|YARN|Hive|Impala|Kafka|AI|ML|R'

def get_soup(url: str):
    r = req.get(url, headers=HEADERS)
    return BeautifulSoup(r.content, 'html5lib')

def get_listings(job_title: str, region: str = "Beglium"):
    """
    Gets the link to all job posts for the given job title & region
    """
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={region}"
    soup = get_soup(url)

    job_links = []
    
    for a in soup.find_all('a', href=True):
        if "view" in a['href']:
            job_links.append(a['href'])
    return job_links

def analyse_listings(job_links: array, job_title: str):
    """
    Gets the job title and required skills from the listing
    """
    jobs = dict()
    job_title = job_title.split(' ')[1]

    for link in job_links:
        title = get_job_title(link)
        if job_title in title.lower():
            required_skills = get_required_skills(link)
            jobs[title] = required_skills
    return jobs
   
def get_job_title(link: str):
    """
    Extracts the job title from the post
    """
    soup = get_soup(link)
    try:
        title = soup.find("h1").text
    except:
        return f"error"
    try:
        return title.split('-')[0]
    except:
        return title

def get_required_skills(link: str):
    """
    Extracts the required skills for the job from the job description
    """
    soup = get_soup(link)
    try:
        div = soup.find("div", attrs={"class":"show-more-less-html__markup"}).text
    except:
        return "something went wrong for {link}"

    cleaned_div = re.sub(r'[\W_]+', ' ', div)
    skills = SKILLS[:-7]
    skills_required = re.findall( skills, cleaned_div, flags=re.IGNORECASE)

    upper_case_skills = SKILLS[-7:]
    skills_required += re.findall( upper_case_skills, cleaned_div)

    return set(skills_required)

def skills_to_list(skills):
    return skills.replace('|',',').split(',')

def create_analytics(job_dict: dict, job_title: str):
    skill_list = skills_to_list(SKILLS)
    analytics = {k:0 for k in skill_list}
    
    for job in job_dict.keys():
        for skill in job_dict[job]:
            try:
                analytics[skill.title()] += 1
            except:
                pass

    analytics['Title'] = job_title
    return analytics

def to_pdf(data):
    return pd.DataFrame.from_dict(data)

if __name__ == "__main__":
    jobs = ["Data analyst", "Data scientist", "Data engineer"]
    region = "Belgium"
    analytics = []
    for job_title in jobs:
        listings = get_listings(job_title, region)
        findings = analyse_listings(listings, job_title )
        job_stats = create_analytics(findings, job_title)
        analytics.append(job_stats)
    
    df = to_pdf(analytics)
    df.to_csv("required_skills.csv")

    



    