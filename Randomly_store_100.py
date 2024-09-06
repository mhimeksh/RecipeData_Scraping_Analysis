import csv
import random

def store_random_recipes(input_filename, output_filename, num_samples=100):
    print(f"[INFO] Reading input CSV file: {input_filename}")


    recipes = []
    recipe_ids = set()
    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            recipes.append({
                'Recipe ID': row.get('Recipe ID'),
                'Ingredient Name': row.get('parsed_Ingredients')
            })
            recipe_ids.add(row.get('Recipe ID'))

    print(f"[INFO] {len(recipes)} rows loaded from the CSV file.")
    print(f"[INFO] {len(recipe_ids)} unique Recipe IDs found.")
    

    recipe_ids_list = list(recipe_ids)
    

    if len(recipe_ids_list) < num_samples:
        raise ValueError("Not enough unique Recipe IDs to sample.")
    

    sampled_recipe_ids = random.sample(recipe_ids_list, num_samples)
    

    filtered_rows = [row for row in recipes if row['Recipe ID'] in sampled_recipe_ids]
    

    with open(output_filename, mode='w', encoding='utf-8') as outfile:
        prev= "#"
        for row in filtered_rows:
            if(row['Recipe ID']!=prev):
                outfile.write('\n')
                prev= row['Recipe ID']
            outfile.write(f"{row['Recipe ID']}—{row['Ingredient Name']}\n")


    
    print(f"[INFO] {len(filtered_rows)} rows saved to {output_filename}")

input_filename = 'parsed_Ingredients.csv' 
output_filename = 'recipes_form.txt'       
store_random_recipes(input_filename, output_filename)
print("[INFO] Recipe extraction and saving completed successfully.")
