import re
import urllib.parse as urlparse
import requests
import json

base_url = "https://crt.sh/?q="


if 'session' not in globals():
    session = requests.Session()

timeout = 25
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Encoding': 'gzip',
}

def get_response(response):
    if response is None:
        return 0
    return response.text if hasattr(response, "text") else response.content


def send_req(url):
    try:
        resp = session.get(url, headers=headers, timeout=timeout)
    except Exception:
        resp = None
    return get_response(resp)


def enumerate(domain):
    query = base_url+domain
    r = send_req(query)
    subdomains = extract_domains(r)

    return subdomains

def extract_domains(resp):
    
    subdomains = set()
    lines = resp.split('<TD style="text-align:center"><A')[1:]
    try:
        for line in lines:
            d = line.split('<TD>')[1].split('</TD>')[0]
            if '*' not in d: subdomains.add(d)
    except Exception:
        pass

    return list(subdomains)


def lambda_handler(event, context):

    domain = event['domain']
    domains = enumerate(domain)
    return {
        'statusCode': 200,
        'body': json.dumps(domains)
    }

