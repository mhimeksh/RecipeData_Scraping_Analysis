import ingredient_parser
import csv

print("[INFO] ingredient_parser loaded successfully.")


def apply_ner_to_ingredients(input_filename, output_filename):

    print(f"[INFO] Reading input CSV file: {input_filename}")
    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    print(f"[INFO] {len(rows)} rows read from the CSV file.")

    filtered_rows = [] 

    # Apply NER to each ingredient
    for index, row in enumerate(rows):
        ingredient_phrase = row.get('ingredient', '')
        ingredient = ingredient_parser.parse_ingredient(ingredient_phrase)


        if ingredient.name:
            row['parsed_Ingredients'] = ingredient.name.text
            filtered_rows.append(row)  # Add only rows with valid `ingredient.name`
        else:
            print(f"[INFO] Skipping row {index + 1} due to missing ingredient name")

        if (index + 1) % 1000 == 0:
            print(f"[INFO] Processed {index + 1} rows")

    print(f"[INFO] Writing NER results to a new CSV file with {len(filtered_rows)} valid rows...")


    fieldnames = reader.fieldnames + ['parsed_Ingredients']
    
    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)  

    print(f"[INFO] NER results saved to {output_filename}")


input_filename = 'unique_ingredients_phrases.csv'
output_filename = 'parsed_Ingredients.csv'
apply_ner_to_ingredients(input_filename, output_filename)
print("[INFO] NER processing completed successfully.")
