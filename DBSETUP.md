DBSETUP.md

```SQL
use STUbry121518;

create table goodreadstemp (
goodreadsid int unsigned,
title varchar(250),
firstname varchar(30),
lastname varchar(30),
isbn varchar(12),
isbn13 varchar(15),
publisher varchar(70),
pages smallint unsigned,
pubyear smallint unsigned,
authorder tinyint unsigned
) engine = InnoDB Default Charset utf8mb4 collate=utf8mb4_unicode_ci;

LOAD DATA LOCAL INFILE 'C:\\TMP\\goodreadscleaned.csv' 
INTO TABLE STUbry121518.goodreadstemp
FIELDS TERMINATED by ','
OPTIONALLY ENCLOSED BY '"';
