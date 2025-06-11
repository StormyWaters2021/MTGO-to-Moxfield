input_file_path = 'deck.dek'
output_file_path = 'cleaned_deck.txt'


def grab_card_info(text, start_delim, end_delim):
    try:
        start_index = text.index(start_delim) + len(start_delim)
        end_index = text.index(end_delim, start_index)
        return text[start_index:end_index]
    except ValueError:
        return ''


new_deck = ''

with open(input_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        test = ""
        qty = grab_card_info(line, 'Quantity="', '"')
        name = grab_card_info(line, 'Name="', '"')
        test += qty + " " + name
        if test == " ":
            test = "OOPS"
        else:
            new_deck += test + "\n"

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(new_deck)

print(f"Cleaned deck exported to '{output_file_path}'.")
