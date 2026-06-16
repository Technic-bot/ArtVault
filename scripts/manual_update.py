import sqlite3 
import argparse
import csv

def proc_opts():
    parser = argparse.ArgumentParser(
            description="Manually update vault db from spreadsheet",
            epilog="Made by Tec with ❤️")
    parser.add_argument("input", help='Input file with entries')
    # Add support for nonsqlite databases in 2050
    parser.add_argument("db", help='Sqlite DB file to update')
    return parser.parse_args()

class ManualUpdater():
    ID_NAME = 'id'
    def __init__(self, file):
        self.file = file

    def read_index(self):
        """ 
        Read existing indices on db, to make sure we are not inserting
        the same post twice

        Not needed if using the unique constraints
        """
        conn = sqlite3.connect(self.file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql_stmt = (f"SELECT id FROM PATREON")
        rows = cursor.execute(sql_stmt).fetchall()
        conn.close()
        
        self.index = set()
        for r in rows:
            self.index.add(int(r['id']))
        print(f"Found {len(self.index)} entries in database")
        return 

    def read_input(self, filename):
        """
            Read input file into program as tuples to update db
        """
        self.posts = [] 
        self.tags = []
        print(f"Reading {filename}")
        with open(filename, 'r') as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                post_id = int(row['id'])
                tup = ( 
                    self.make_tuple(row)
                )
                self.posts.append(tup)

                tags = self.make_tags(row['tags'])
                for tag in tags:
                    tag_tup = (post_id, tag)
                    self.tags.append(tag_tup)
        print(f"Found {len(self.posts)} posts")
        print(f"Found {len(self.tags)} individual tags")
        return

    def count_entries(self):
        """ 
            Get numbers of post on db
        """
        conn = sqlite3.connect(self.file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql_stmt = "SELECT count(id) as cuenta FROM PATREON;"
        row = cursor.execute(sql_stmt).fetchone()
        conn.close()

        return int(row['cuenta'])

    def make_tuple(self, row):
        """ Turn row dict into tuple """ 
        tup = ( int(row['id']),
            row['title'].strip("\" "),
            row['description'].strip("\" "),
            row['filename'].strip("\" "),
            row['type'].strip("\" "),
            row['src_url'].strip("\" "),
            row['date'].strip("\" "),
        )
        return tup
    
    def make_tags(self, tags):
        """ process tags string into list """
        raw_tags = tags.split(',')
        proc_tags = [tag.strip("\" ") for tag in raw_tags]
        return proc_tags
    
    def persist(self):
        """ Save read data into database """
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        sql_stmt = ("INSERT OR REPLACE INTO patreon " 
                    "(id, title, description, filename, type, "
                    "src_url, date) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?);")
        cursor.executemany(sql_stmt, self.posts)

        sql_stmt = ("INSERT OR REPLACE INTO tags (id, tag) "
                    "VALUES (?, ?);")
        cursor.executemany(sql_stmt, self.tags)
        conn.commit()
        conn.close()

if __name__=="__main__":
    opts = proc_opts()
    updater = ManualUpdater(opts.db)    
    updater.read_input(opts.input)
    before = updater.count_entries()
    updater.persist()
    after = updater.count_entries()
    print(f"Post in {opts.db}")
    print(f"Post before: {before}")
    print(f"Post after: {after}")
    print(f"{after-before} posts added")
