# /usr/bin/env python
import argparse 

import json
import csv

import time
import random

import httpx


def proc_opts():
    parser = argparse.ArgumentParser(
        description="Process patreon JSON and output CSV file.",
        epilog="Made by Tec with love")
    parser.add_argument("infile", help="Input json from patreon api")
    parser.add_argument("outfile", help="Output csv with processed data")
    return parser.parse_args()


def parse_entry(entry):
    """ Return a post dictionary from entry """
    post = entry['attributes']
    typ = post['post_type']
    title = post['title']
    if typ != 'image_file':
        print(f"Got no image file {title}")
        return {}
    post_id = entry['id']
    tags = parse_tags(entry['relationships'])
    filename = download_img(post['post_file']['url'])
    print(f"Got Post: {title}")
    post_dic = {
        'id' : post_id,
        'title' : title,
        #'download' : post['post_file']['url'],
        'filename' : filename,
        'type' : typ,
        'src_url' : post['url'],
        'date' : post['published_at'],
        'description' : post['content'],
        'tags' : tags
    }
    return post_dic


def download_img(url):
    r = httpx.head(url)
    status = r.status_code
    if status != 200:
        logger.error(f"Access denied: {status}")
        return

    content_disp = r.headers['content-disposition']
    for c in content_disp.split(';'):
        if 'filename' in c:
            filename = c.split('=')[1].strip('\"')
            break

    eep = random.uniform(0.5, 1.5)
    time.sleep(eep)
    return filename


def parse_tags(post):
    """ Get the tags of this post """
    raw_tags = post['user_defined_tags']['data']
    tag_list = []
    for tag in raw_tags:
        tag_name = tag['id'].split("user_defined;")[1]
        tag_list.append(tag_name)
    return ','.join(tag_list)


def parse_patreon(infile):
    post_list = []
    with open(infile, 'r') as json_file:
        data = json.load(json_file)
        entries = data['data']
        for entry in entries:
            post = parse_entry(entry)
            if post:
                post_list.append(post)
    print(f"Got {len(post_list)} posts")
    return post_list


def persist_posts(posts, outfile):
    fields = list(posts[0].keys())
    with open(outfile, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(posts)
    return


if __name__=="__main__":
    args = proc_opts()
    posts = parse_patreon(args.infile)
    persist_posts(posts, args.outfile)

