import requests
from bs4 import BeautifulSoup



def get_last_page(url):
  result=requests.get(url)
  soup=BeautifulSoup(result.text, "html.parser")
  pages=soup.find("div",{"class":"s-pagination"}).find_all("a")
  last_page=pages[-2].get_text(strip=True)
  return int(last_page)

def extract_job(html):
  title=html.find("h2", {"class":"mb4"}).find("a")["title"]
  company_row =html.find("h3", {
                                "class":"fc-black-700"
                               }).find_all(
                                "span", recursive=False)
  company=company_row[0].get_text(strip=True)
  location=company_row[1].get_text(strip=True)
  job_id=html.find("h2", {"class":"mb4"}).find("a")["href"][6:12]
  apply_link=f"https://stackoverflow.com/jobs/{job_id}"
  return {
    'title':title, 
    'company':company, 
    'location':location,
    'apply_link':apply_link
  }

def extract_jobs(last_page, url):
  jobs=[]
  for page in range(last_page):
    result=requests.get(f"{url}&pg={page+1}")
    soup=BeautifulSoup(result.text, "html.parser")
    results=soup.find_all("div", {"class":"grid--cell fl1"})
    for result in results:
      job=extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs2(word):
  url=f"https://stackoverflow.com/jobs?id=518970&q={word}+&l=Berlin"
  last_page=get_last_page(url)
  jobs=extract_jobs(last_page, url)
  #print(last_page)
  return jobs