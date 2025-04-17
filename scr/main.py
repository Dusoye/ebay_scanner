
import time
from sheet_loader import load_reference
from ebay_client   import search_ebay, process_results
from data_store    import load_seen, save_seen
from notifier      import send_discord_alert


def main_loop(interval=60):
    seen = load_seen()
    while True:
        df = load_reference()
        for _, row in df.iterrows():
            query = row['item']
            max_price = row['max_price']
            results = search_ebay(query)
            matches = process_results(query, max_price, results)
            for match in matches:
                if match['itemId'] not in seen:
                    send_discord_alert(match)
                    seen.add(match['itemId'])
        save_seen(seen)
        time.sleep(interval)

if __name__ == '__main__':
    main_loop()