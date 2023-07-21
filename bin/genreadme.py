import json


def get_packages_list() -> str:
    with open('packages.json', 'r', encoding='utf-8') as f:
        file_content = json.load(f)
        for package in file_content['packages']:
            package_markdown = [
                '- [%s](%s)' % (package['name'], package['details'])
            ]

            markdown.append('\n'.join(package_markdown))

    return '\n'.join(markdown)


markdown = []
markdown.append('# My Sublime Text Packages\n')
markdown.append(get_packages_list())

with open('README.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(markdown))
