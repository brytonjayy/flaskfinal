delimiter $
create procedure getbookbyid(bookid INT)
BEGIN
    IF bookid > 0 THEN
        SELECT gb.book_id, gb.title,gb.isbn,gb.isbn13,gb.pubyear,gp.pubname
        FROM grbooks gb
        JOIN grpublishers gp ON (gp.publisher_id=gb.publisher_id)
        WHERE gb.book_id = bookid;    
    END IF;
END $

create procedure getbooksbytitle(booktitle char(200))
BEGIN
DECLARE searchterm CHAR(201);
set searchterm = "%";
IF CHAR_LENGTH(booktitle) > 0 THEN
set searchterm = concat(booktitle,'%');
SELECT gb.book_id, gb.title,gb.isbn,gb.isbn13,gb.pubyear,gp.pubname
FROM grbooks gb
JOIN grpublishers gp ON (gp.publisher_id=gb.publisher_id)
WHERE gb.title LIKE searchterm;    
END IF;
END $

create procedure getauthors(letter CHAR(30))
BEGIN
DECLARE searchterm CHAR(31);
set searchterm = "%";
IF CHAR_LENGTH(letter) > 0 THEN
  set searchterm = concat(letter,'%');
END IF;
SELECT ga.lastname, ga.firstname, ga.author_id
FROM grauthors ga
WHERE ga.lastname like searchterm
ORDER BY ga.lastname;
END $

create procedure getbooksbyauthid(authid INT)
BEGIN
    IF authid > 0 THEN
        SELECT gb.book_id, gb.title,gb.isbn,gb.isbn13,gb.pubyear,gp.pubname
        FROM grbooks gb
        JOIN grpublishers gp ON (gp.publisher_id=gb.publisher_id)
        JOIN grbooks_authors gba ON (gba.book_id = gb.book_id)
        WHERE gba.author_id = authid
        ORDER BY gb.title;    
    END IF;
END $

create procedure getpublishers(letter CHAR(30))
BEGIN
DECLARE searchterm CHAR(31);
set searchterm = "%";
IF CHAR_LENGTH(letter) > 0 THEN
  set searchterm = concat(letter,'%');
END IF;
SELECT gp.publisher_id, gp.pubname
FROM grpublishers gp
WHERE gp.pubname like searchterm
ORDER BY gp.pubname;
END $

create procedure getauthorsbybookid(bookid INT)
BEGIN
    IF bookid > 0 THEN
        SELECT ga.author_id, ga.lastname, ga.firstname,gba.authorder
        FROM grbooks_authors gba JOIN grauthors ga ON (gba.author_id = ga.author_id)
        WHERE gba.book_id = bookid
        ORDER BY gba.authorder;
    END IF;
END $

create procedure getbookbyisbn(bookisbn char(15))
BEGIN
    IF CHAR_LENGTH(bookisbn) > 0 THEN
        SELECT gb.book_id, gb.title,gb.isbn,gb.isbn13,gb.pubyear,gp.pubname
        FROM grbooks gb
        JOIN grpublishers gp ON (gp.publisher_id=gb.publisher_id)
        WHERE gb.isbn = bookisbn OR gb.isbn13 = bookisbn;    
    END IF;
END $

create procedure getbooksbypubid(pubid INT)
BEGIN
    IF pubid > 0 THEN
        SELECT gb.book_id, gb.title,gb.isbn,gb.isbn13,gb.pubyear,gp.pubname
        FROM grbooks gb
        JOIN grpublishers gp ON (gp.publisher_id=gb.publisher_id)
        WHERE gb.publisher_id = pubid
        ORDER BY gb.title;    
    END IF;
END $

create procedure getbooksbyyear(yearpub INT)
BEGIN
    IF yearpub > 0 THEN
        SELECT gb.book_id, gb.title,gb.isbn,gb.isbn13,gb.pubyear,gp.pubname
        FROM grbooks gb
        JOIN grpublishers gp ON (gp.publisher_id=gb.publisher_id)
        WHERE gb.pubyear = yearpub
        ORDER BY gb.title;    
    END IF;
END $


create procedure addauthorsbooks(booktitle CHAR(200), fname CHAR(30), lname CHAR(30), authord INT)
BEGIN
    DECLARE bookid INT;
    DECLARE authid INT;
    set bookid = 0;
    set authid = 0;

    select author_id  into authid
    from grauthors
    where firstname = fname
    AND lastname = lname;

    select book_id into bookid from grbooks
    where title = booktitle;

    IF bookid > 0 and authid > 0  THEN
        INSERT INTO grbooks_authors (book_id, author_id, authorder)
        Values (bookid, authid, authord); 
    ELSE
        signal SQLSTATE '45000' set MESSAGE_TEXT = "Invalid title and/or author information";
    END IF;
END $

create procedure getauthorsbyname(lname CHAR(30), fname CHAR(30))
BEGIN
DECLARE lnamesearch CHAR(31);
DECLARE fnamesearch CHAR(31);
set lnamesearch = "";
set fnamesearch = "";

IF locate("%",lname) != 0 THEN
signal SQLSTATE '45000' set MESSAGE_TEXT = "Invalid % sign in lname string";
/* set lnamesearch = "Stohlman";  */
ELSEIF  CHAR_LENGTH(lname) > 0 THEN
  set lnamesearch = concat(lname,'%');
END IF;

IF CHAR_LENGTH(fname) > 0 THEN
  set fnamesearch = concat(fname,'%');
ELSE
  set fnamesearch = "%";
END IF;

SELECT ga.author_id, ga.lastname, ga.firstname
FROM grauthors ga
WHERE ga.lastname like lnamesearch
AND ga.firstname like fnamesearch
ORDER BY ga.lastname;
END $
delimiter ;

delimiter ;