create database moshu;

create table Users 
(
	id int primary key auto_increment,
	
	username varchar(18) not null,
	
	_password varchar(18) not null,  #password为Dbeaver关键字，多加了一个_
	
    avatar varchar(255) not null, #存储头像文件的路径，多个路径间用'$'隔开
    
    name varchar(18) not null,
    
    email varchar(18) not null,
    
    gnum int not null, #团队数
    
    profile text #简介
);

create table _Groups             #Groups为Dbeaver关键字，多加了一个_
(
	id int primary key auto_increment,

	name varchar(18) not null,

	unum int not null,          #成员数

	pnum int not null,			#团队数

	profile text
);

create table Members      
(
	gid int not null,

	uid int not null,

	_role int not null 		#role为关键字，多加一个r #0代表普通成员，1代表管理员，2代表创建者（超级管理员）
);

create table Projects 
(
	id int primary key auto_increment,

	name varchar(18) not null,

	available int not null, #0代表可用，1代表在回收站

	status int not null, #0代表正在进行，1代表已结束

	gid int not null,

	uid int,

	starttime datetime not null,
	
	endtime datetime not null,

	prototype varchar(255), #存储设计原型文件的路径，多个路径间用'$'隔开

	uml varchar(255), #同上

	document varchar(255) #同上
);

alter table Members add constraint fk1 foreign key Members(gid) references _Groups(id) ON DELETE CASCADE ON UPDATE cascade;

alter table Members add constraint fk2 foreign key Members(uid) references Users(id) ON delete CASCADE ON UPDATE cascade;

alter table Projects add constraint fk3 foreign key Projects(gid) references _Groups(id) ON DELETE CASCADE ON UPDATE cascade;

alter table Projects add constraint fk4 foreign key Projects(uid) references Users(id) ON delete SET NULL ON UPDATE cascade;
