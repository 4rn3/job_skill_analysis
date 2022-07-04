import re 
import pandas as pd
import requests as req

from pandas import array
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

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

def analyse_listings(job_links: array):
    """
    Gets the job title and required skills from the listing
    """
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
    skills = '|Master|Bachelor|bachelordiploma|masterdiploma|SQL|Python|SAS|Pyspark|AWS|GCP|Google|Amazon|Azure|Excel|Power|Tableau|QlikView|Hadoop|Spark|docker|kubernetes|Oracle|Pandas|Dash|Scikit|TensorFlow|Keras|git|Airflow|Java|Golang|warehouse|lake|Modeling|Linux|Cloudera|HDFS|YARN|Hive|Impala|Kafka'
    skills_required = re.findall( skills, cleaned_div, flags=re.IGNORECASE)

    upper_case_skills = "AI|ML|R"
    skills_required += re.findall( upper_case_skills, cleaned_div)

    return set(skills_required)

def create_analytics(job_dict: dict):
    skill_list = ['Master', 'Bachelor', 'SQL', 'Python', 'SAS', 'AWS', 'GCP', 'Google', 'Amazon', 'Azure', 'Excel', 'Power', 'Tableau', 'QlikView', 'Hadoop', 'Spark', 'docker', 'kubernetes', 'Oracle', 'Pandas', 'Dash', 'Scikit', 'TensorFlow', 'Keras', 'git', 'Airflow', 'Java', 'Golang', 'data_warehouse', 'data_lake', 'data_Modeling', 'Linux', 'Cloudera', 'HDFS', 'YARN', 'Hive', 'Impala', 'Kafka']
    data_analyst = {k:0 for k in skill_list}
    data_scientist = {k:0 for k in skill_list}
    data_engineer = {k:0 for k in skill_list}

    for job in job_dict.keys():
        if "analyst" in job.lower() or "analist" in job.lower():
            for skill in job_dict[job]:
                data_analyst[skill] += 1
        if "science" in job.lower() :
            pass
    print(data_analyst)


if __name__ == "__main__":
    #listings = get_listings("Data Analyst", "Belgium")
    #findings = analyse_listings(listings)
    #print(findings)
    job_dict = {'Data Analyst': {'master', 'Excel', 'dash', 'R', 'excel', 'Power'}, 'Data Analyst ': {'dash', 'R'}, 'Business Data Analyst Junior': {'SQL', 'dash', 'power'}, 'Junior Data Analyst (Growth)': {'SQL', 'Python', 'power', 'Tableau', 'Google', 'git', 'R', 'excel'}, 'Junior Data Analyst': {'SQL', 'master', 'Excel', 'Bachelor', 'excel', 'Power'}, 'Google Data Analyst': {'SQL', 'Python', 'dash', 'Bachelor', 'Tableau', 'Google', 'git', 'R', 'Warehouse'}, 'DATA & INSIGHTS ANALYST ': 'something went wrong', 'something went wrong for https://be.linkedin.com/jobs/view/data-analyst-at-nexeo-3103947600?refId=JkStqlwbWRmNaMBj6tGeCQ%3D%3D&trackingId=blcOK01Eg6xyJkv64pG9jg%3D%3D&position=12&pageNum=0&trk=public_jobs_jserp-result_search-card': 'something went wrong', 'something went wrong for https://be.linkedin.com/jobs/view/data-analyst-at-colruyt-group-3129239618?refId=JkStqlwbWRmNaMBj6tGeCQ%3D%3D&trackingId=CIBk%2F1KxEUK%2FxeelklKsjQ%3D%3D&position=13&pageNum=0&trk=public_jobs_jserp-result_search-card': {'SQL', 'Python', 'master', 'dash', 'R'}, 'Business Data Analyst': {'Bachelor', 'R', 'Master'}, 'Junior Clinical Data Analyst': {'power', 'Excel', 'R', 'excel', 'SAS'}, 'Data Analyst/Analytical Engineer': {'sas', 'SQL', 'modeling', 'Azure', 'Master', 'git', 'R', 'lake', 'Power'}, 'something went wrong for https://be.linkedin.com/jobs/view/data-analyst-at-gentis-recruitment-3136683329?refId=JkStqlwbWRmNaMBj6tGeCQ%3D%3D&trackingId=foPtTl6KG6dbu%2F5U%2Bi8NOg%3D%3D&position=19&pageNum=0&trk=public_jobs_jserp-result_search-card': 'something went wrong', 'something went wrong for https://be.linkedin.com/jobs/view/data-analyst-at-select-hr-3079977987?refId=JkStqlwbWRmNaMBj6tGeCQ%3D%3D&trackingId=qm5VEJ1O8727TTB3TT8tRg%3D%3D&position=20&pageNum=0&trk=public_jobs_jserp-result_search-card': 'something went wrong', 'Data analyst': {'R', 'Master'}, 'Consumer Journey Data Analyst': {'Excel', 'dash', 'Bachelor', 'git', 'R', 'Power'}, 'Data Analist': {'SQL', 'master', 'Excel', 'Bachelor', 'Tableau', 'git', 'SAS', 'Power', 'warehouse'}}
    create_analytics(job_dict)


    