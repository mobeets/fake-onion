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

def get_msg(mdl, max_length=140, max_tries=1000, \
    max_overlap_total=6, max_overlap_ratio=0.5, text=''):
    
    msg = None
    while msg is None or msg in text:
        msg = mdl.make_short_sentence(max_length, tries=max_tries, \
            max_overlap_total=max_overlap_total, \
            max_overlap_ratio=max_overlap_ratio)
    return msg

def get_model(infile=DATAFILE_ONION):
    text = load(infile)
    return markovify.NewlineText(text, state_size=2), text

def markov(infile=DATAFILE_ONION, n=20):
    text_model, text = get_model(infile)
    for i in xrange(n):
        print get_msg(text_model, text=text)

def combine(infiles=[DATAFILE_DOI, DATAFILE_ONION], n=20):
    ts = []
    mdls = []
    for infile in infiles:
        mdl, text = get_model(infile)
        ts.append(text)
        mdls.append(mdl)

    M = markovify.combine(mdls, weights=[1.0, 0.4])
    for i in xrange(n):
        print get_msg(M, text='\n'.join(ts))

if __name__ == '__main__':
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    # combine(n=N)
    markov(n=N)

    # less data/headlines.txt | grep "suspiciously funny phrase"
