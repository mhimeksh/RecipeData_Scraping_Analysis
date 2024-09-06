import csv


def add_header_to_csv(input_filename, output_filename, new_header):


    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)


    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(new_header)  
        writer.writerows(rows)  

    print(f"[INFO] New header added and data saved to {output_filename}")


def assign_ids_to_csv(input_filename, output_filename):

    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        recipes = list(reader)


    for index, recipe in enumerate(recipes):
        recipe['Recipe ID'] = f"Recipe {index + 1}"


    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Recipe ID'] + reader.fieldnames  
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(recipes)

    print(f"[INFO] Recipe IDs assigned and saved to {output_filename}")


input_filename = 'recipes_tastecom.csv'
output_filename = 'recipes_tastecom_with_ids.csv'
new_header = ['Title', 'URL', 'Ingredients', 'Instructions', 'Region Cuisine', 'Servings', 'Prep Time'] 
add_header_to_csv(input_filename, output_filename, new_header)
assign_ids_to_csv(output_filename, output_filename)
