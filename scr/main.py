
import time
from sheet_loader import load_reference
from ebay_client   import search_ebay, process_results
from data_store    import load_seen, save_seen
from notifier      import send_discord_alert


def main():
    """
    Load the sheet, scan eBay, send any new alerts, then exit.
    """
    seen = load_seen()
    df   = load_reference()

    for _, row in df.iterrows():
        query     = row['item']
        max_price = row['max_price']
        results   = search_ebay(query)
        matches   = process_results(query, max_price, results)

        for match in matches:
            if match['itemId'] not in seen:
                send_discord_alert(match)
                seen.add(match['itemId'])

    save_seen(seen)

if __name__ == '__main__':
    main()