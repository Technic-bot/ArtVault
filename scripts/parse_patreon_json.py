# /usr/bin/env python
import argparse 
import os

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
    parser.add_argument("--download-dir", help="Folder to download images to")
    parser.add_argument("--pages", type=int, help="How many pages to process")
    return parser.parse_args()

class PatreonParser():
    def __init__(self, download_dir):
        self.download_dir = download_dir
        return

    def parse_entry(self, entry):
        """ Return a post dictionary from entry """
        post = entry['attributes']
        typ = post['post_type']
        title = post['title']
        if typ != 'image_file':
            print(f"Got no image file {title}")
            return {}
        try:
            post_id = entry['id']
            tags = self.parse_tags(entry['relationships'])
            filename = self.download_img(post['post_file']['url'])
            print(f"Got Post: {title} - {filename}")
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
        except KeyError as err:
            print(entry)
        return post_dic

    def download_img(self, url):
        r = httpx.head(url)
        status = r.status_code
        if status != 200:
            print(f"Access denied: {status}")
            return

        content_disp = r.headers['content-disposition']
        for c in content_disp.split(';'):
            if 'filename' in c:
                filename = c.split('=')[1].strip('\"')
                break

        eep = random.uniform(0.5, 1.5)
        time.sleep(eep)

        if self.download_dir:
            file_path = self.download_dir + filename
            if not os.path.isfile(file_path):
                # print(f"Downloading {url}")
                r = httpx.get(url)
                with open(self.download_dir + filename, mode='wb') as file:
                    print(f"Saving {filename} to {self.download_dir}")
                    file.write(r.content)
            else:
                print(f"{filename} exists skipping")

        return filename

    def parse_tags(self, post):
        """ Get the tags of this post """
        raw_tags = post['user_defined_tags']['data']
        tag_list = []
        for tag in raw_tags:
            tag_name = tag['id'].split("user_defined;")[1]
            tag_list.append(tag_name)
        return ','.join(tag_list)

    def parse_patreon(self, infile):
        with open(infile, 'r') as json_file:
            data = json.load(json_file)
        return data

    def parse_entries(self, data):
        post_list = []
        entries = data['data']
        self.next_page = data['links']['next']
        for entry in entries:
            post = self.parse_entry(entry)
            if post:
                post_list.append(post)
        print(f"Got {len(post_list)} posts")
        return post_list

    def persist_posts(self, posts, outfile):
        fields = list(posts[0].keys())
        with open(outfile, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(posts)
        return

    def get_next_page(self):
        r = httpx.get(self.next_page)
        status = r.status_code
        if status != 200:
            print(f"Access denied from {next_entry_url}: {status}")
            return
        next_json = r.json()
        return next_json


if __name__=="__main__":
    args = proc_opts()
    patreon = PatreonParser(args.download_dir)
    data = patreon.parse_patreon(args.infile)
    posts = patreon.parse_entries(data)
    patreon.persist_posts(posts, args.outfile)

