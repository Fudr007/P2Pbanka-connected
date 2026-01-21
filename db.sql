create table bank(
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  host_ip varchar(11) NOT NULL CHECK(REGEXP_LIKE(host_ip, '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')),
  port INT NOT NULL CHECK(port >= 65525 AND port <= 65535)
);

CREATE SEQUENCE seq_acc_number
  START WITH 10000
  INCREMENT BY 1
  MAXVALUE 99999
  NOCYCLE;

create table bank_account(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    balance int default 0 check(balance >= 0),
    acc_number NUMBER(5) DEFAULT seq_acc_number.NEXTVAL UNIQUE
);