import requests
from bs4 import BeautifulSoup
import time
import re

def scrape_portfolio(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = session.get(url, headers=headers)
        time.sleep(5)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve portfolio. Error: {e}")
        return None
    
    if response.status_code != 200:
        print(f"Failed to retrieve portfolio. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    name = "Name Not Found"
    name_elem = soup.find('h1', {'class': 'name'})
    if name_elem:
        name = name_elem.text.strip()
    else:
       
        text_content = soup.get_text(separator=' ')
        match =  match = re.search(r'\bI\s*am\s+([A-Za-z\s]+)|\bI\'m\s+([A-Za-z\s]+)', text_content)
        if match:
         name = match.group(1).strip() if match.group(1) else match.group(2).strip()
    
    education_elem = soup.find('section', {'id': 'education'})
    education = education_elem.text.strip() if education_elem else 'Education Not Found'

    experience_elem = soup.find('section', {'id': 'experience'})
    experience = experience_elem.text.strip() if experience_elem else 'Experience Not Found'

    skills_elem = soup.find('section', {'id': 'skills'})
    skills = skills_elem.text.strip() if skills_elem else 'Skills Not Found'
    
    return {
        'name': name,
        'education': education,
        'experience': experience,
        'skills': skills
    }

def generate_resume(data):

    template = f"""
    ----------------------
    Resume Generated from Portfolio
    ----------------------
    Name: {data['name']}
    
    Education:
    {data['education']}
    
    Experience:
    {data['experience']}
    
    Skills:
    {data['skills']}
    ----------------------
    """
    return template

def main():

    portfolio_url = input("Enter portfolio URL: ").strip()
    
    profile_data = scrape_portfolio(portfolio_url)
    
    if profile_data:

        resume = generate_resume(profile_data)
        print(resume)
    else:
        print("Failed to generate resume.")

if __name__ == "__main__":
    main()
