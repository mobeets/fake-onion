import json
import urllib

URL = "http://api.crossref.org/works?filter=type:journal-article&cursor={cursor}&rows=50"
OUTFILE = 'data/doi.txt'

def get_titles(items):
    return [item['title'][0] for item in items if len(item['title']) > 0]

def write(titles, outfile):
    titles = list(set(titles))
    with open(outfile, 'w') as f:
        f.write('\n'.join(titles).encode('utf-8'))

def main(outfile=OUTFILE):
    titles = []
    cursor = "*"
    for i in xrange(20):
        x = json.loads(urllib.urlopen(URL.format(cursor=cursor)).read())
        y = x['message']
        ts = get_titles(y['items'])
        titles.extend(ts)
        for title in ts:
            print title
        cursor = y['next-cursor']
    write(titles, outfile)


if __name__ == '__main__':
    main()
