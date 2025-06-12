import csv
import requests
import time

input_csv = 'deck.csv'
output_txt = 'deck_fixed.txt'

scryfall_api_url = 'https://api.scryfall.com/cards/mtgo/'
headers = {
    'User-Agent': 'MTGO2Moxfield/1.0',
    'Accept': '*/*'
}


def fetch_card_data(mtgo_id):
    url = f'{scryfall_api_url}{mtgo_id}'
    response = requests.get(url, headers=headers)
    time.sleep(0.075)
    if response.status_code == 200:
        return response.json(), False
    return None, False


def try_with_fallback(mtgo_id):
    card_data, fallback = fetch_card_data(mtgo_id)
    if card_data:
        return card_data, fallback
    try:
        fallback_id = int(mtgo_id) - 1
        card_data, _ = fetch_card_data(fallback_id)
        if card_data:
            return card_data, True
    except ValueError:
        pass
    return None, False


def process_csv(input_csv, output_txt):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        with open(output_txt, mode='w', encoding='utf-8') as output_file:
            for row in reader:
                quantity = row.get('Quantity', '').strip()
                card_name = row.get('Card Name', '').strip()
                set_name = row.get('Set', '').strip()
                mtgo_id = row.get('ID #', '').strip()
                premium = row.get('Premium', '').strip().lower() == 'yes'
                fallback_flag = False

                if set_name == 'PRM':
                    if not mtgo_id.isdigit():
                        print(f"Error: Invalid MTGO ID '{mtgo_id}' for '{card_name}'")
                        continue

                    card_data, used_fallback = try_with_fallback(mtgo_id)

                    if card_data:
                        collector_number = card_data.get('collector_number', 'N/A')
                        fallback_flag = used_fallback
                    else:
                        print(f"Error: No card found for MTGO ID {mtgo_id} or {int(mtgo_id)-1}")
                        continue
                else:
                    raw_collector = row.get('Collector #', '').strip()
                    collector_number = raw_collector.split('/')[0]

                line = f"{quantity} {card_name} ({set_name}) {collector_number}"
                if fallback_flag or premium:
                    line += " *F*"

                output_file.write(line + '\n')

    print(f"Deck fixed and saved to {output_txt}")


process_csv(input_csv, output_txt)
