-- To be run from root of repo
-- sqlite3 db/twokinds_patreon.db  < scripts/create_schema.sql
CREATE TABLE IF NOT EXISTS "patreon_tmp"(
    "vault_id" INTEGER primary key,
    "id" INTEGER,
    "title" TEXT,
    "description" TEXT,
    "filename" TEXT,
    "type"  TEXT,
    "src_url" TEXT,
    "date" TEXT,
    unique(id, filename)
);

CREATE TABLE IF NOT EXISTS "tags_tmp"(
    "id" INTEGER,
    "tag" TEXT,
    unique(id, tag)
);


INSERT INTO patreon_tmp 
    (id, title, description, filename, type, src_url, date)
    SELECT id, title, description, filename, type, src_url, date from patreon;

INSERT INTO tags_tmp
    (id, tag) 
    SELECT id, tag from tags;

-- ALTER TABLE patreon RENAME to patreon_orig;
-- DROP TABLE patreon;
-- ALTER TABLE patreon_tmp RENAME to patreon;

-- ALTER TABLE tags RENAME to tags_orig;
-- DROP TABLE tags;
-- ALTER TABLE tags_tmp RENAME to tags;
