import os
import sys
import pandas
import time
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get best result from hmmscan result.')
    parser.add_argument('-g', '--gene', help='gene3d hmmscan result')
    parser.add_argument('-f', '--funfam', help='funfam hmmscan result')
    parser.add_argument('-o','--output',help='Output file name', default='ID_cath_map.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.gene):
        print "gene3d hmmscan result not found."
        sys.exit(1)

    if not os.path.exists(args.funfam):
        print "funfam hmmscan result not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def main():

    process_options()

    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'b_E-value', 'b_score', 'b_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    funfam_df =  pandas.read_csv(args.funfam, delim_whitespace=True, comment='#', names=col, engine='python')
    gene_df = pandas.read_csv(args.gene, delim_whitespace=True, comment='#', names=col, engine='python')

    funfam_df = funfam_df.drop_duplicates(['query']).loc[:,['target','query']].loc[:,['target','query']].set_index(['query'])
    gene_df = gene_df.drop_duplicates(['query']).loc[:,['target','query']].loc[:,['target','query']].set_index(['query'])

    funfam_df['sf'] = funfam_df['target'].apply(lambda x: x.split('/')[0])
    funfam_df['funfam'] = funfam_df['target'].apply(lambda x: x.split('/')[2])
    gene_df['model'] = gene_df['target'].apply(lambda x: x.split('|')[2].split('/')[0])

    funfam_df = funfam_df.drop('target',1)
    gene_df = gene_df.drop('target',1)
    result_df = funfam_df.join(gene_df)

    result_df.to_csv(args.output, sep='\t')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
