create table author0(
        author_Id int NOT NULL PRIMARY KEY,
		firstname,
        lastname,
		/** multi line
			test comment **/
        age
		
    );

    create table book0(
		book_Id int NOT NULL PRIMARY KEY,
        title,
		-- test comment
        author,
        published,
		FOREIGN KEY(author) REFERENCES author0(author_Id) 
    );