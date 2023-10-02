import argparse

import json

import os
import shutil
import glob

from dataclasses import dataclass, field, asdict

# Program to clean download jsons from patreon downloader fork

@dataclass
class PatreonPost():
    post_id: int
    title: str
    description: str
    filename: str
    post_type: str
    patreon_url: str
    publication_date: str
    tags: list[str]= field(default_factory=list)

def proc_opts():
    parser = argparse.ArgumentParser(description='This programs helps clean patreon downloads')
    parser.add_argument('indir',help='Input directory')
    parser.add_argument('outdir',help='Input directory')
    parser.add_argument('--json',help='Name of json db file',default='twokinds_patreon.json')
    return parser.parse_args()

def filter_page(page):
    posts = []
    for post in page['data']:
        attrs=post['attributes']
        if attrs['embed']:
            # this keeps stuff like polls to get added 
            continue
        user_tags = post['relationships']['user_defined_tags']
        post_tags = [t['id'].split(';')[-1] for t in user_tags['data']]
        try:
            post = PatreonPost(post_id=post['id'],
                                title = attrs['title'],
                                description = attrs['content'], 
                                filename = attrs['post_file']['name'],
                                post_type = attrs['post_type'],
                                tags = post_tags,
                                patreon_url= attrs['image']['url'],
                                publication_date = attrs['published_at'])
            posts.append(post)
        except TypeError as e:
            print(f"Malformed entry: {post['id']} {attrs['title']} ")
        except KeyError as e:
            print(e)
            print(f"Malformed entry : {post['id']} {attrs['title']} ")

    return posts

def get_all_jsons(folder):
    jsons = glob.iglob(folder+"*.json")
    all_posts = []
    for j in jsons:
        with open(j,'r') as json_file:
            print(f"Reading {j}")
            page_json = json.load(json_file)
            page_post = filter_page(page_json)
            all_posts.extend(page_post)

    return all_posts

def copy_art(patreon,in_dir,out_dir):
    """ Get all images and rename and move to output folder"""
    for p in patreon:
        local_path = in_dir + p.post_id + '_post_' + p.filename 
        
        if os.path.isfile(local_path):
            out_path = out_dir + p.filename
            if not os.path.isfile(out_path):
                shutil.copyfile(local_path, out_path)
        else:
            print(f"{local_path} not found on local disk")
        
    return
     

def persist_patreon_json(patreon, filename):
    print(f"Saving to {filename}") 
    with open(filename,'w') as out_file:
        json.dump(patreon,out_file,default=asdict)
    

if __name__=="__main__":
    args =  proc_opts()
    patreon_jsons = get_all_jsons(args.indir) 
    copy_art(patreon_jsons, args.indir, args.outdir)
    persist_patreon_json(patreon_jsons,args.json)
    # 
    
