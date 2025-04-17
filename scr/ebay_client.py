import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

# Replace with your eBay AppID (App Name) from developer.ebay.com
API_ENDPOINT = 'https://svcs.ebay.com/services/search/FindingService/v1'
API_KEY      = os.getenv('EBAY_API_KEY')
# Cosine-similarity threshold (0 to 1)
COSINE_SIM_THRESHOLD = 0.5


def search_ebay(query):
    headers = {
        'X-EBAY-SOA-SECURITY-APPNAME': API_KEY,
        'X-EBAY-SOA-OPERATION-NAME': 'findItemsByKeywords',
        'X-EBAY-SOA-RESPONSE-DATA-FORMAT': 'JSON'
    }
    params = {
        'keywords': query,
        'paginationInput.entriesPerPage': 10,
        'itemFilter(0).name': 'ListingType',
        'itemFilter(0).value': 'FixedPrice'
    }
    resp = requests.get(API_ENDPOINT, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()


def process_results(reference_item, max_price, results):
    """
    Returns a list of matches {'itemId','title','price','similarity','url'}
    where price <= max_price and similarity >= threshold.
    """
    try:
        items = results['findItemsByKeywordsResponse'][0]['searchResult'][0].get('item', [])
    except KeyError:
        items = []

    titles = [it['title'][0] for it in items]
    if not titles:
        return []

    # Compute cosine similarity
    vectorizer = TfidfVectorizer().fit([reference_item] + titles)
    ref_vec = vectorizer.transform([reference_item])
    title_vecs = vectorizer.transform(titles)
    sims = cosine_similarity(ref_vec, title_vecs).flatten()

    matches = []
    for idx, it in enumerate(items):
        price = float(it['sellingStatus'][0]['currentPrice'][0]['__value__'])
        if price <= max_price and sims[idx] >= COSINE_SIM_THRESHOLD:
            item_id = it['itemId'][0]
            url = f"https://www.ebay.com/itm/{item_id}"
            matches.append({
                'itemId': item_id,
                'title': it['title'][0],
                'price': price,
                'similarity': sims[idx],
                'url': url
            })
    return matches