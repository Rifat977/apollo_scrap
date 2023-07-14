import csv

def remove_rows_from_csv(source_file, reference_file, id_column):
    with open(source_file, 'r') as source_csv_file:
        source_csv_reader = csv.DictReader(source_csv_file)
        source_rows = list(source_csv_reader)

    with open(reference_file, 'r') as reference_csv_file:
        reference_csv_reader = csv.DictReader(reference_csv_file)
        reference_ids = set(row[id_column] for row in reference_csv_reader)

    filtered_rows = [row for row in source_rows if row[id_column] not in reference_ids]

    output_file = 'filtered_data.csv'
    with open(output_file, 'w', newline='') as output_csv_file:
        fieldnames = source_csv_reader.fieldnames
        writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Filtered data has been written to '{output_file}'.")

source_file = 'filtered_data1.csv'
reference_file = 'filtered_data2.csv'
id_column = 'id'

remove_rows_from_csv(source_file, reference_file, id_column)
