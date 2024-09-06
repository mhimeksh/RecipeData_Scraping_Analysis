import requests
from bs4 import BeautifulSoup
import time
import csv
import os


#Extracts the cuisine from tags of a recipe page
def extract_cuisine(soup):

    cuisine_keywords = [
        'asian', 'british', 'middle eastern', 'european', 'italian', 'america', 'american', 'africa',
        'australian', 'australia', 'african', 'indian', 'india', 'chinese', 'china', 'mexican',
        'japanese', 'korean', 'thai', 'vietnamese', 'french', 'spanish', 'greek', 'turkish',
        'mediterranean', 'lebanese', 'moroccan', 'caribbean', 'jamaican', 'cuban', 'brazilian',
        'argentinian', 'peruvian', 'colombian', 'portuguese', 'german', 'russian', 'swedish',
        'filipino', 'malaysian', 'indonesian', 'singaporean', 'egyptian', 'ethiopian', 'iranian',
        'pakistani', 'bangladeshi', 'syrian', 'iraqi', 'palestinian', 'israeli', 'tunisian', 'algerian',
        'nigerian', 'south african', 'kenyan', 'ghanaian', 'polish', 'hungarian', 'romanian',
        'slovak', 'czech', 'belgian', 'dutch', 'austrian', 'swiss', 'danish', 'norwegian', 'finnish'
    ]


    lozenge_tags = soup.find_all('a', class_='lozenge')


    for tag in lozenge_tags:
        tag_text = tag.get_text(strip=True).lower()  
        for keyword in cuisine_keywords:
            if keyword in tag_text:  
                print(f"Found matching cuisine: {tag_text}")
                return tag_text.capitalize()  


    print("No matching cuisine found. Assigning 'Other'.")
    return 'Other'

#Scrape the recipe page of taste.com for recipe information
def scrape_recipe_page(url):

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'No Title'


                ingredients = [ingredient.get_text(strip=True) for ingredient in soup.find_all('div', class_='ingredient-description')]


                instructions = [instruction.get_text(strip=True) for instruction in soup.find_all('div', class_='recipe-method-step-content')]

 
                cuisine = extract_cuisine(soup)

                cooking_info = soup.find('ul', class_='recipe-cooking-info')


                prep_time = None
                servings = None


                if cooking_info:
                    for li in cooking_info.find_all('li'):
                        label = li.get_text(strip=True).lower()
                        if 'prep' in label:
                            prep_time = li.find('span').get_text(strip=True)  
                        elif 'serves' in label:
                            servings = li.find('span').get_text(strip=True)  
                
                region_cuisine = cuisine if cuisine else 'No Region/Cuisine'
                servings = servings if servings else 'No Servings'
                prep_time = prep_time if prep_time else 'No Prep Time'
                
                print(f"\n[INFO] Recipe '{title}' extracted successfully.")
                return {
                    'title': title,
                    'url': url,
                    'ingredients': ', '.join(ingredients),
                    'instructions': ' '.join(instructions),
                    'region_cuisine': region_cuisine,
                    'servings': servings,
                    'prep_time': prep_time
                }

        except requests.RequestException as e:
            print(f"[ERROR] Request failed (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(2 ** attempt)
    print(f"[ERROR] Failed to retrieve recipe page {url} after {max_retries} attempts")
    return None

#Scrape the recipe collection page for the url of recipe pages on that page
def scrape_page(page_number):
    url = f"https://www.taste.com.au/recipes/collections/budget?page={page_number}&q=&sort=recent"

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                recipe_links = []

                recipe_cards = soup.find_all('li', class_=['col-xs-6 top', 'col-xs-6'])
                for card in recipe_cards:
                    a_tag = card.find('a', href=True)
                    if a_tag:
                        link = a_tag['href']
                        if link.startswith('/'):
                            link = 'https://www.taste.com.au' + link
                        recipe_links.append(link)
        
                print(f"[INFO] Found {len(recipe_links)} recipes on page {page_number}.")
                return recipe_links

        except requests.RequestException as e:
            print(f"[ERROR] Request failed (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(2 ** attempt)
    print(f"[ERROR] Failed to retrieve page {page_number} after {max_retries} attempts")
    return None

#Append the scraped recipes to recipes_tastecom.csv
#This is called after every collection page
def save_to_csv(data, filename='recipes_tastecom.csv'):
    file_exists = os.path.isfile(filename)
    keys = data[0].keys()
    

    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        if not file_exists:
            dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"[INFO] Finished writing to {filename}")

def main():
    all_recipe_data = []
    
    for page_number in range(1, 529):
        print(f"[INFO] Scraping page {page_number}...")
        recipe_links = scrape_page(page_number)
        page_recipe_data = []
        
        if recipe_links:
            for recipe_link in recipe_links:
                recipe_data = scrape_recipe_page(recipe_link)
                if recipe_data:
                    page_recipe_data.append(recipe_data)

        if page_recipe_data:
            save_to_csv(page_recipe_data) 
            all_recipe_data.extend(page_recipe_data)
        


if __name__ == "__main__":
    main()
