import markovify
# import pandas as pd

DATAFILE = 'data/headlines.txt'

def parse(infile='data/theonion.csv', outfile=DATAFILE):

    df = pd.read_csv(infile)
    titles = df[~df['title'].isnull()]['title'].values
    with open(outfile, 'w') as f:
        f.write('\n'.join(titles))

def markov(infile=DATAFILE):
    with open(DATAFILE) as f:
        text = f.read()

    # Build the model.
    text_model = markovify.NewlineText(text, state_size=3)

    # Print five randomly-generated sentences
    for i in range(5):
        sent = text_model.make_sentence(tries=1000, \
            max_overlap_total=6, max_overlap_ratio=0.5)
        if sent is not None:
            print sent

    # Print three randomly-generated sentences of no more than 140 characters
    # for i in range(3):
    #     sent = text_model.make_short_sentence(140)
    #     if sent is not None:
    #         print sent

if __name__ == '__main__':
    markov()
