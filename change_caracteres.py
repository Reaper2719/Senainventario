import pandas as pd
import unicodedata

def remove_accents_and_replace_n(string):
    # Normalize and remove accents
    nfkd_form = unicodedata.normalize('NFKD', string)
    without_accents = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    # Replace 'Ñ' with 'n'
    return without_accents.replace('Ñ', 'n').replace('ñ', 'n')

# Load your Excel file (replace 'your_file.xlsx' with your actual file name)
file_path = 'Centros_formacion_Nacional_2024.xlsx'  # Change to your file path
df = pd.read_excel(file_path)

# Apply the function to all string cells in the DataFrame
df = df.apply(lambda col: col.map(remove_accents_and_replace_n) if col.dtype == "object" else col)

# Save the modified DataFrame to a new Excel file
df.to_excel('Centros2024.xlsx', index=False)
