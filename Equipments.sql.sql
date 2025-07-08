create database Equipments
go

use  Equipments
go

create table Equipments(
number bigint,
E_type char(50),
E_name char(50),
price  float,
inDate bigint,
isBad int,
badDate bigint,
primary key (number)
)

insert into Equipments values(0,'²âÁ¿ÒÇÆ÷','Á¿±­',23.5,20250625,0,0);
insert into Equipments values(1,'·ÖÎöÒÇÆ÷','ºìÍâ¹âÆ×ÒÇ',2300.0,20250625,0,0);
insert into Equipments values(2,'¼ÆÁ¿ÒÇÆ÷','ÓÎ±ê¿¨³ß',28.5,20250625,0,0);
insert into Equipments values(3,'ÖÆ±¸ÒÇÆ÷','³¬Éù²¨ÇåÏ´Æ÷',230.0,20250625,0,0);


select *  from Equipments

delete from Equipments
where number=10


