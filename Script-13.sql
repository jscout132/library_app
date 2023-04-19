select * from "user" 

select COUNT(genre) from books 
where genre ='History'

select title from books 
where genre='History'

alter table librarian 
rename column pin to id

alter table books 
add column year_published INTEGER;

update books 
set binding = 'hardcover'
where isbn = '9780062363602'

update books 
set "length" = 230
where isbn = '9781419732517'

alter table books
add column lib_id VARCHAR(10) references librarian(id)

select * from "user"