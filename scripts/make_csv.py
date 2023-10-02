import argparse

import pandas as pd 

def proc_opts():
  parser = argparse.ArgumentParser('Twokinds Patreon CSV db generator')
  parser.add_argument('file', help='Patreon raw json')
  parser.add_argument('patreon', help='Patreon csv')
  parser.add_argument('tags', help='Tags extra file')
  return parser.parse_args()

def get_tags(df):
    tags_df = df['tags'].sort_values() 
#    tags_df.drop_duplicates(inplace=True)
    return tags_df

def get_csv_df(df):
    """ Makes a csv, clean version of the df"""
    clean_df = df.drop('tags',axis=1)
    return clean_df

if __name__ == "__main__":
    args = proc_opts()
    
    patreon_df = pd.read_json(args.file)
    print("Dataframe cols")
    print(patreon_df.columns)
    patreon_df.set_index('post_id',inplace=True)
    print(f"Got {len(patreon_df)} entries in {args.file}")
    patreon_df.drop('download_url',axis=1, inplace=True)

    exploded_df = patreon_df.explode('tags')
    tags = get_tags(exploded_df)
    tags.to_csv(args.tags)

    clean_df = get_csv_df(patreon_df) 
    clean_df.to_csv(args.patreon)
