import json
import os
import re
import urllib.request


def download_repository_details(api_url: str, access_token: str):
    # Set the API URL
    api_url = api_url.replace('https://github.com/', 'https://api.github.com/repos/')

    # Set headers to include the authentication token
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        # Create a request with headers
        request = urllib.request.Request(api_url, headers=headers)

        # Make the GET request to the GitHub API
        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                repository_details = json.loads(response.read().decode())

                return repository_details
            else:
                print(f"Error: Unable to fetch repository details. Status code: {response.status}")
                return None

    except urllib.error.URLError as e:
        print(f"Error: {e.reason}")
        return None


def get_access_token():
    with open(os.path.expanduser('~/.config/gh/hosts.yml'), 'r', encoding='utf-8') as f:
        match = re.search('oauth_token: (.+)', f.read())
        if match:
            return match.group(1)

    print("Error: No access_token found")
    return None


def cache_repository_details(repository: str, content: dict) -> None:
    if not os.path.isdir('tmp'):
        os.makedirs('tmp')

    cache_file = re.sub('[^a-zA-Z0-9-]', '_', repository.replace('https://github.com/', ''))
    with open(f'tmp/{cache_file}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(content))


def create_cache_file_name(repository_url: str) -> str:
    cache_file = re.sub('[^a-zA-Z0-9-]', '_', repository_url.replace('https://github.com/', ''))

    return f'tmp/{cache_file}.json'


def get_repository_details(package: dict, access_token: str) -> dict:
    repository_url = package['details']
    cache_file_name = create_cache_file_name(repository_url)
    if os.path.isfile(cache_file_name):
        print(f'Found cache {cache_file_name}')
        with open(cache_file_name, 'r', encoding='utf-8') as f:
            repository_details = json.loads(f.read())
    else:
        print(f'Downloading {repository_url}')
        repository_details = download_repository_details(repository_url, access_token)
        repository_details['package_control'] = package
        cache_repository_details(repository_url, repository_details)

    return repository_details


def get_packages() -> list:
    with open('packages.json', 'r', encoding='utf-8') as f:
        return json.load(f)['packages']

    return []


access_token = get_access_token()

markdown = []
markdown.append('# Packages')
markdown.append('')

for package in get_packages():
    repository_details = get_repository_details(package, access_token)
    print(f"  Repository Name: {repository_details['name']}")
    markdown.append(
        '- [%s](%s) %s' % (
            repository_details['package_control']['name'],
            repository_details['package_control']['details'],
            repository_details['description']
        )
    )

markdown.append('')

with open('PACKAGES.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(markdown))
