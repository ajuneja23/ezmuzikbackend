CREATE TABLE users( 
username text unique not null,
password text not null,
user_id text unique not null,
primary key(user_id)
);

create table queries(
query text not null,
searchdate datetime not null,
user_id text not null,
foreign key(user_id) references users(user_id)
);