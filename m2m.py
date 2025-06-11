import csv

input_csv = 'deck.csv'
output_txt = 'deck_fixed.txt'

columns = ['Quantity', 'Card Name', 'Set', 'Collector #']

with open(input_csv, mode='r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)

    with open(output_txt, mode='w', encoding='utf-8') as output_file:
        for row in reader:
            card_data = []
            for col in columns:
                columntext = row.get(col, '')
                if col == 'Collector #':
                    columntext = columntext.split('/')[0]
                elif col == 'Set':
                    columntext = f"({columntext})"
                card_data.append(columntext)

            output_file.write(' '.join(card_data) + '\n')

print(f"Deck fixed and saved to {output_txt}")
