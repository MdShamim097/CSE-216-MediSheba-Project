create table "HOSPITAL"
(
    "HOSPITAL_ID"   NUMBER(10)    not null
        constraint HOSPITAL_ID_PK
            primary key,
    "HOSPITAL_NAME" VARCHAR2(255) not null,
    "LOCATION"      VARCHAR2(255),
    "CAPACITY"      NUMBER(10),
    "Available_Cabin" NUMBER(10),
    "FIRST_NAME" VARCHAR2(255) not null ,
    "LAST_NAME" VARCHAR2(255) not null ,
    "PASSWORD" VARCHAR2(255) not null,
    "GENDER" VARCHAR2(1) not null ,
    "EMAIL" VARCHAR2(255) not null,
    "PHONE" VARCHAR2(255)
);
create table "DOCTOR"
(
    "DOCTOR_ID"           NUMBER(10)    not null
        constraint DOCTOR_PK
            primary key,
    "FIRST_NAME"          VARCHAR2(255) not null,
    "LAST_NAME"           VARCHAR2(255) not null,
    "EMAIL"               VARCHAR2(255) not null,
    "PASSWORD"            VARCHAR2(255) not null,
    "SPECIALIZATION"      VARCHAR2(255),
    "PHONE"               VARCHAR2(255),
    "BLOOD_GROUP"         VARCHAR2(2),
    "isBLOOD_AVAILABLE" VARCHAR2(1),
    "GENDER"              VARCHAR2(1)   not null,
    "FEES"                NUMBER(10),
    "HOSPITAL_ID"         NUMBER(10) CONSTRAINT D_HOSPITAL_ID_FK REFERENCES HOSPITAL,
    "LOCATION" VARCHAR2(255)
);

create table "USERS"
(
    "USER_ID"           NUMBER(10)    not null
        constraint USERS_PK
            primary key,
    "FIRST_NAME"        VARCHAR2(255) not null,
    "LAST_NAME"         VARCHAR2(255) not null,
    "EMAIL"             VARCHAR2(255) not null,
    "PASSWORD"          VARCHAR2(255) not null,
    "PHONE"             VARCHAR2(255),
    "BLOOD_GROUP"       VARCHAR2(2),
    "ISBLOOD_AVAILABLE" VARCHAR2(1),
    "GENDER"            VARCHAR2(1)   not null
);

create table "BLOOD_BANK"
(
    "BLOOD_BANK_ID" NUMBER(10)    not null
        constraint BLOOD_BANK_PK
            primary key,
    "NAME"          VARCHAR2(255) not null,
    "A+"          NUMBER(10),
    "A-"          NUMBER(10),
    "B+"          NUMBER(10),
    "B-"          NUMBER(10),
    "O+"          NUMBER(10),
    "O-"          NUMBER(10),
    "AB+"         NUMBER(10),
    "AB-"         NUMBER(10),
    "FIRST_NAME" VARCHAR2(255) not null,
    "LAST_NAME" VARCHAR2(255) not null ,
    "PASSWORD" VARCHAR2(255) not null ,
    "GENDER" VARCHAR2(1) not null ,
    "EMAIL" VARCHAR2(255) not null ,
    "PHONE" VARCHAR2(255),
    LOCATION VARCHAR2(255)
);

create table "DOCTOR_USER_HISTORY"
(
    "DOCTOR_ID" NUMBER(10) not null
        constraint DUH_DOCTOR_ID_FK
            references DOCTOR,
    "USER_ID"   NUMBER(10) not null
        constraint DUH_USER_ID_FK
            references USERS,
    "RATING"    NUMBER(10),
    "TIME"      DATE
);

create table "CABIN"
(
    "CABIN_ID" NUMBER(10) not null
        constraint CABIN_PK
            primary key,
    "PRICE"    NUMBER(10),
    "CATEGORY" VARCHAR2(255),
    "IS_AVAILABLE" VARCHAR2(1),
    "USER_ID"   NUMBER(10) 
        constraint CAB_USER_ID_FK
            references USERS,
    "ENTRY_DATE" DATE,
    "EXIT_DATE" DATE,
    "HOSPITAL_ID"   NUMBER(10) CONSTRAINT D_HOSPITAL_ID_FK REFERENCES HOSPITAL
);
create table "DOCTOR_BBANK_HISTORY"
(
    "BLOOD_BANK_ID"     NUMBER(10)  not null
        constraint BLOOD_BANK_ID_FK
            references BLOOD_BANK,
    "DOCTOR_ID"         NUMBER(10)  not null
        constraint DOCTORS_ID_FK
            references DOCTOR,
    "DATES"             DATE        not null,
    "DONATEorRECEIVE" VARCHAR2(1) not null
);

create table "HOSPITAL_USER_HISTORY"
(
    "USER_ID"     NUMBER(10) not null
        constraint HU_USER_ID_FK
            references USERS,
    "HOSPITAL_ID" NUMBER(10) not null
        constraint HU_HOSPITAL_ID_FK
            references HOSPITAL,
    "CABIN_ID"    NUMBER(10) not null
        constraint HU_CABIN_ID_FK
            references CABIN,
    "START_DATE"  DATE NOT NULL ,
    "END_DATE"    DATE NOT NULL ,
    "COST"        NUMBER(10)
);

create table "USER_BBANK_HISTORY"
(
    "BLOOD_BANK_ID"     NUMBER(10)  not null
        constraint U_BLOOD_BANK_IDS_FK
            references BLOOD_BANK,
    "USER_ID"           NUMBER(10)  not null
        constraint U_USER_IDS_FK
            references USERS,
    "DATES"             DATE        not null,
    "DONATEorRECEIVE" VARCHAR2(1) not null
);


CREATE SEQUENCE HOSPITAL_SEQ START WITH 1;

CREATE OR REPLACE TRIGGER HOSPITAL_TRIGGER BEFORE INSERT ON HOSPITAL
    FOR EACH ROW
    BEGIN
        SELECT HOSPITAL_SEQ.nextval
        INTO :NEW.HOSPITAL_ID
        FROM DUAL;
    end;


CREATE SEQUENCE DOCTOR_SEQ START WITH 1;

CREATE OR REPLACE TRIGGER DOCTOR_TRIGGER BEFORE INSERT ON DOCTOR
    FOR EACH ROW
    BEGIN
        SELECT DOCTOR_SEQ.nextval
            INTO :NEW.DOCTOR_ID
        FROM DUAL;
    end;


CREATE SEQUENCE USERS_SEQ START WITH 1;

CREATE TRIGGER USERS_TRIGGER BEFORE INSERT
    ON USERS FOR EACH ROW
    BEGIN
        SELECT USERS_SEQ.nextval
            INTO :NEW.USER_ID
        FROM DUAL;
    end;
CREATE SEQUENCE BLOOD_BANK_SEQ START WITH 1;

CREATE TRIGGER BLOOD_BANK_TRIGGER
    BEFORE INSERT ON BLOOD_BANK
    FOR EACH ROW BEGIN
    SELECT BLOOD_BANK_SEQ.nextval
        INTO :NEW.BLOOD_BANK_ID
        FROM DUAL;
end;


CREATE SEQUENCE CABIN_SEQ START WITH 1;

create trigger CABIN_TRIGGER
    before insert
    on CABIN
    for each row
BEGIN
    SELECT CABIN_SEQ.nextval
    INTO :NEW.CABIN_ID
    FROM DUAL;
end;
