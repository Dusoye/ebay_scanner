# eBay Alert Bot

A modular Python project that automates the process of scanning eBay "Buy It Now" listings based on a dynamic reference list stored in Google Sheets. It filters deals by price and title similarity, logs which items have already been alerted on, and sends notifications to a Discord channel.

## Features

- **Dynamic Reference List**: Loads search terms and maximum prices from a public Google Sheets CSV.
- **eBay API Integration**: Queries the eBay Finding API for fixed-price listings matching each search term.
- **Cosine Similarity Matching**: Uses TF-IDF and cosine similarity to ensure titles closely match the reference terms.
- **Duplicate Alert Prevention**: Tracks seen `itemId`s in a local CSV so each deal is only alerted once.
- **Discord Notifications**: Sends formatted alerts to a Discord channel via webhook.
- **Modular Design**: Easily swap out components (e.g. Sheets access, datastore, notifier) or extend functionality.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dusoye/ebay_scanner.git
   cd ebay_scanner
   ```

2. **Install dependencies**
   ```bash
   pip install requests pandas scikit-learn
   ```

## Configuration

1. **Google Sheets**
   - Publish your sheet as CSV: **File → Share → Publish to web → CSV**.
   - Copy the generated CSV URL and paste it into `sheet_loader.py`:
     ```python
     SHEET_CSV_URL = (
         "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"
         "/export?format=csv&gid=0"
     )
     ```

2. **eBay API**
   - Sign up for an eBay Developer account and create an application to get your AppID.
   - In `ebay_client.py`, set your AppID:
     ```python
     API_KEY = 'YOUR_EBAY_APP_ID'
     ```

3. **Discord Webhook**
   - Create a webhook in your Discord server (**Server Settings → Integrations → Webhooks**).
   - Copy the webhook URL and set it in `notifier.py`:
     ```python
     DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'
     ```

## Usage

Run the main script in a loop to continuously poll for new deals:

```bash
python main.py
```

By default, `main.py` polls every 60 seconds. You can adjust the interval by passing a different value:

```python
# In main.py
main_loop(interval=120)  # Poll every 2 minutes
```

## File Structure

```
ebay-alert-bot/
├── sheet_loader.py    # Loads items & max prices from Google Sheets CSV
├── ebay_client.py     # eBay API wrapper + cosine similarity matching
├── data_store.py      # Reads/writes seen item IDs to seen_items.csv
├── notifier.py        # Sends messages to Discord via webhook
├── main.py            # Orchestrates loading, searching, alerting in a loop
├── seen_items.csv     # Generated at runtime: logged item IDs
└── README.md          # This documentation
```

## Customization

- **Thresholds**: Adjust `COSINE_SIM_THRESHOLD` in `ebay_client.py` to loosen or tighten title matching.
- **Result Pagination**: Modify `paginationInput.entriesPerPage` or add pagination logic to cover more results.
- **Alternate Notifiers**: Replace `notifier.py` with SMS, email, or other chat integrations.
- **Datastore**: Swap CSV in `data_store.py` for SQLite or another database for scalability.

## Deployment

For production, deploy on AWS (EC2, Lambda) or GCP (Compute Engine, Cloud Functions) and use a scheduler (cron, Cloud Scheduler) to run `main.py` at desired intervals. Ensure environment variables or secure vaults store your keys and webhook URLs.

## Contributing

Contributions, issues, and feature requests are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

