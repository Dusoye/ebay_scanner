import csv
import os

SEEN_CSV = 'seen_items.csv'


def load_seen():
    """Returns a set of itemIds already alerted on."""
    if not os.path.exists(SEEN_CSV):
        return set()
    with open(SEEN_CSV, newline='') as f:
        reader = csv.reader(f)
        return set(row[0] for row in reader)


def save_seen(seen_set):
    """Writes the current set of seen itemIds to CSV."""
    with open(SEEN_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        for item_id in seen_set:
            writer.writerow([item_id])