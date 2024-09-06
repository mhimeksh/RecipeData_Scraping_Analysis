import csv

def fetch_unique_ingredients(input_filename, output_filename):

 
    recipe_ingredients = []  

    try:

        with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                ingredients_set = set() 

                
                recipe_id = row.get('Recipe ID', '')
                ingredients = row.get('Ingredients', '')  

                if not recipe_id or not ingredients:
                    print(f"Missing data in row: {row}")  
                    continue
                
                ingredient_list = [ingredient.strip() for ingredient in ingredients.split(',') if ingredient.strip()]


                for ingredient in ingredient_list:
                    if ingredient not in ingredients_set:
                        ingredients_set.add(ingredient)
                        recipe_ingredients.append({'Recipe ID': recipe_id, 'ingredient': ingredient})

    except FileNotFoundError:
        print(f"[ERROR] The file {input_filename} does not exist.")
        return
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        return

    # Write the unique ingredient entries to a new CSV file
    fieldnames = ['Recipe ID', 'ingredient']
    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(recipe_ingredients)

    print(f"[INFO] Unique ingredient entries saved to {output_filename}")

# Example usage
input_filename = 'recipes_tastecom_with_ids.csv'
output_filename = 'unique_ingredients_phrases.csv'
fetch_unique_ingredients(input_filename, output_filename)
