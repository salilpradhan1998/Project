# We're going to scrape https://github.com/
# We'll geta list of topics. For each topusc, we'll get topic title, URL 
# For each topic we will get the top 25 repos for the topic page
# For each repos we will grab the repo name, stars and repo URL
# At the end we will create the csv
from distutils import text_file
from operator import index
from matplotlib import use
from matplotlib.pyplot import axis
import requests
from bs4 import BeautifulSoup as bf
import pandas as pd

topic_url = 'https://github.com/topics'
topic_page = requests.get(topic_url)
page_content = topic_page.text
soup = bf(page_content, 'html.parser')
topic_title_tags = soup.find_all('p', 
    {'class':"f3 lh-condensed mb-0 mt-1 Link--primary"}) #as the lenght if p tags is 67, we have to find something else
topic_description = soup.find_all('p',
    {'class':"f5 color-fg-muted mb-0 mt-1"})
topic_links = soup.find_all('a',
    {'class':"no-underline flex-grow-0"})
topic_title = []
for tags in topic_title_tags:
    topic_title.append(tags.text)
topic_descriptions = []
for des in topic_description:
    topic_descriptions.append(des.text.strip())
topic_url = []
base_url = 'https://github.com'
for tag in topic_links:
    topic_url.append(base_url + tag['href'])
topic_dict = {'Topic_name':topic_title, 'Topic_description': topic_descriptions,
                'Topic_URL': topic_url}
topic_df = pd.DataFrame(topic_dict)
topic_df.to_csv('Github Trending Topic.csv', index= None)
number_stars = []
project_names = []
name = []
topics_link = []
final_links = []
for link in topic_url:
    intopic = requests.get(link)
    topic_doc = bf(intopic.text, 'html.parser')
    intopic_most_star = topic_doc.find_all('h3', {'class':'f3 color-fg-muted text-normal lh-condensed'})


    for tags in range(len(intopic_most_star)):
        top_repo = intopic_most_star[tags].find_all('a')
        name.append(top_repo[0].text.strip())
        final_links.append(base_url + top_repo[1]['href'])
        project_names.append(top_repo[1].text.strip())
    stars_count = topic_doc.find_all('span', {'id':"repo-stars-counter-star"})
    for i in range(len(stars_count)):
        star_number = stars_count[i].text
        star = star_number[:-1]
        stars = float(star)*1000
        number_stars.append(stars)       
    dict2 = {'User Name':name , 'Projct Name': project_names, 'Number of Stars': number_stars, 'Links to the Project':final_links}
    df1 = pd.DataFrame(dict2)
    final_df = pd.concat([topic_df, df1], axis =1)
    final_df.to_excel('Github Treanding topic.xlsx')

    

            



