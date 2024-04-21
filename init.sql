create table student(
    id varchar(8) primary key,
    grade int,
    department varchar(20),
    credit int,
    check_init int
);

create table course(
    id varchar(4) primary key,
    coursename varchar(20),
    compulsory int,
    department varchar(20),
    courseTime int,
    credit int,
    maxstudent int,
    nowstudent int
);

create table schedule(
    id int primary key auto_increment,
    studentId varchar(8),
    courseId int
);

create table account(
    studentId varchar(8) primary key,
    passwd varchar(10)
);

insert into student(id,grade,department,credit,check_init) values("d1234567",2,"computer science",0,0);
insert into student(id,grade,department,credit,check_init) values("d1150254",2,"computer engineer",0,0);
insert into student(id,grade,department,credit,check_init) values("d0000000",2,"computer science",0,0);

insert into account(studentId,passwd) values("d1234567","1234567");
insert into account(studentId,passwd) values("d1150254","1150254");
insert into account(studentId,passwd) values("d0000000","0000000");

-- computer science
INSERT INTO course (id, coursename, compulsory, department, courseTime, credit, maxstudent, nowstudent)
VALUES
('2003', '系統程式', 1, 'computer science', 113, 3, 10, 5),
('3022', '資料庫系統', 1, 'computer science', 224, 3, 10, 3),
('2025', '機率與統計', 1, 'computer science', 424, 3, 10, 4),
('2072', 'Web程式設計', 0, 'computer science', 368, 3, 10, 5),
('2026', '電子商務安全', 0, 'computer science', 368, 3, 10, 7),
('2030', '電子商務安全', 0, 'computer science', 524, 3, 10, 9),
('2014', '資料結構', 1, 'computer science', 268, 3, 10, 5),
('1323', '互聯網路', 0, 'computer science', 468, 3, 10, 5),
('1332', '數位系統設計', 0, 'computer science', 568, 3, 10, 5),
('1334', 'UNIX應用與實務', 0, 'computer science', 312, 2, 10, 5),
('1328', '多媒體系統', 0, 'computer science', 334, 2, 10, 5),
('1348', '人工智慧導論', 0, 'computer science', 168, 3, 10, 5),
('1357', '軟體框架設計', 0, 'computer science', 168, 3, 10, 5);

-- computer engineer
INSERT INTO course (id, coursename, compulsory, department, courseTime, credit, maxstudent, nowstudent)
VALUES
('2001', '工程數學', 1, 'computer engineer', 113, 3, 10, 5),
('2049', '電子學', 1, 'computer engineer', 224, 3, 10, 5),
('2009', '電路學', 1, 'computer engineer', 324, 3, 10, 5),
('2011', '電磁學', 1, 'computer engineer', 268, 3, 10, 5),
('2012', '微處理機系統', 1, 'computer engineer', 424, 3, 10, 5),
('2020', '系統程式', 0, 'computer engineer', 168, 3, 10, 5),
('2018', '電波工程概論', 0, 'computer engineer', 168, 3, 10, 5),
('2019', '機率論', 0, 'computer engineer', 379, 3, 10, 5),
('2627', '半導體元件', 0, 'computer engineer', 469, 4, 10, 5),
('2632', '電力電子', 0, 'computer engineer', 514, 4, 10, 5);