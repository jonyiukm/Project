/*============================================================================*/
/* DBMS: PostgreSQL 9*/
/* Created on : 9/25/2018 9:25:21 PM                                           */
/*============================================================================*/


/*============================================================================*/
/*                                  TABLES                                    */
/*============================================================================*/
CREATE TABLE CATEGORIES (
  CAT_ID              CHARACTER(3) NOT NULL,
  CAT_DESC            CHARACTER(15) NOT NULL,
CONSTRAINT PK_CATEGORIES PRIMARY KEY (CAT_ID)
);

CREATE TABLE BUSINESS_CATEGORY (
  BIZ_ID            CHARACTER(5) NOT NULL,
  BIZ_DESC          CHARACTER(30),
  CAT_ID            CHARACTER(3),
CONSTRAINT PK_BUSINESS_CATEGORY PRIMARY KEY (BIZ_ID)
);

CREATE TABLE PROVINCE (
  PROV_ID           CHARACTER(5) NOT NULL,
  PROV_DESC         CHARACTER(20),
CONSTRAINT PK_PROVINCE PRIMARY KEY (PROV_ID)
);

CREATE TABLE CITY (
  CITY_ID           CHARACTER(5) NOT NULL,
  CITY_NAME         CHARACTER(25),
CONSTRAINT PK_CITY PRIMARY KEY (CITY_ID)
);

CREATE TABLE STORE_LOCATION (
  STORE_ID          CHARACTER(10) NOT NULL,
  BIZ_ID            CHARACTER(5) NOT NULL,
  PROV_ID           CHARACTER(5),
  CITY_ID           CHARACTER(5),
  ADDRESS           CHARACTER(30),
  POSTAL_CODE       CHARACTER(6),
  LATITUDE          INTEGER,
  LONGITUDE         REAL,
  TYPES             VARCHAR(65),
CONSTRAINT PK_STORE_LOCATION PRIMARY KEY (STORE_ID)
);

/*============================================================================*/
/*                                 INDEXES                                    */
/*============================================================================*/
CREATE UNIQUE INDEX IDX_CAT_ID_IDX_CATEGORIES ON CATEGORIES(CAT_ID ASC)
;

CREATE UNIQUE INDEX IDX_BIZ_ID_IDX_BUSINESS_CATEGORY ON BUSINESS_CATEGORY(BIZ_ID ASC)
;

CREATE  INDEX IDX_PROV_ID_IDX_PROVINCE ON PROVINCE(PROV_ID ASC)
;

CREATE  INDEX IDX_CITY_ID_IDX_CITY ON CITY(CITY_ID ASC)
;

CREATE  INDEX IDX_STORE_ID_IDX_STORE_LOCATION ON STORE_LOCATION(STORE_ID ASC)
;

/*============================================================================*/
/*                               FOREIGN KEYS                                 */
/*============================================================================*/
ALTER TABLE BUSINESS_CATEGORY
    ADD CONSTRAINT FK_REFERENCE_5
        FOREIGN KEY (CAT_ID)
            REFERENCES CATEGORIES (CAT_ID)
 ;


ALTER TABLE STORE_LOCATION
    ADD CONSTRAINT FK_REFERENCE_2
        FOREIGN KEY (PROV_ID)
            REFERENCES PROVINCE (PROV_ID)
 ;

ALTER TABLE STORE_LOCATION
    ADD CONSTRAINT FK_REFERENCE_3
        FOREIGN KEY (CITY_ID)
            REFERENCES CITY (CITY_ID)
 ;

ALTER TABLE STORE_LOCATION
    ADD CONSTRAINT FK_REFERENCE_4
        FOREIGN KEY (BIZ_ID)
            REFERENCES BUSINESS_CATEGORY (BIZ_ID)
 ;


