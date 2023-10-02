-- To be run from root of repo
-- sqlite3 db/twokinds_patreon.db  < scripts/create_schema.sql
drop table patreon;
drop table tags;

CREATE TABLE IF NOT EXISTS "patreon"(
    "id" INTEGER PRIMARY KEY,
    "title" TEXT,
    "description" TEXT,
    "filename" TEXT,
    "type"  TEXT,
    "patreon_url" TEXT,
    "date" TEXT
);

CREATE TABLE IF NOT EXISTS "tags"(
    "id" INTEGER,
    "tag" TEXT
);

.mode csv
.import data/dev/twokinds_patreon.csv patreon
.import data/dev/twokinds_patreon_tags.csv tags
