import markovify

RAWFILE = 'data/theonion.csv'
DATAFILE_ONION = 'data/headlines.txt'
DATAFILE_DOI = 'data/doi.txt'

def parse(infile=RAWFILE, outfile=DATAFILE_ONION):
    import pandas as pd
    df = pd.read_csv(infile)
    titles = df[~df['title'].isnull()]['title'].values
    with open(outfile, 'w') as f:
        f.write('\n'.join(titles))

def load(infile):
    with open(infile) as f:
        return f.read()

def generate(mdl, n, text=''):
    c = 0
    while c < n:
        sent = mdl.make_short_sentence(140, tries=1000, \
            max_overlap_total=6, max_overlap_ratio=0.5)
        if sent is not None and sent not in text:
            c += 1
            print sent

def markov(infile=DATAFILE_ONION, n=20):
    text = load(infile)
    text_model = markovify.NewlineText(text, state_size=2)
    generate(text_model, n, text)

def combine(infiles=[DATAFILE_DOI, DATAFILE_ONION], n=20):
    ts = []
    mdls = []
    for infile in infiles:
        text = load(infile)
        ts.append(text)
        mdl = markovify.NewlineText(text, state_size=2)
        mdls.append(mdl)

    M = markovify.combine(mdls, weights=[1.0, 0.01])
    generate(M, n, '\n'.join(ts))

if __name__ == '__main__':
    # combine()
    markov()

    # less data/headlines.txt | grep "suspiciously funny phrase"
