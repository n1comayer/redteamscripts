import argparse
from urllib.request import urlopen, urlparse
from urllib.error import HTTPError, URLError
import ssl
import encodings.idna

def scan_git_repo(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc or parsed_url.path  # Extract hostname from URL
        url_domain = ".".join(encodings.idna.ToASCII(part).decode("ascii") for part in hostname.strip().split("."))

        for protocol in ['https://', 'http://']:
            try:
                response = urlopen(''.join([protocol, url_domain, '/.git/HEAD']), context=ssl._create_unverified_context(), timeout=5)
                content = response.read(200).decode('utf-8', 'ignore')
                if 'refs/heads' in content:
                    print(''.join(['[*] Found: ', protocol, url_domain]))
                    return
            except (HTTPError, URLError):
                continue
    except Exception as e:
        print(f'Error scanning {url}: {e}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help='URL or hostname to scan')
    args = parser.parse_args()
    scan_git_repo(args.url)

if __name__ == '__main__':
    main()

