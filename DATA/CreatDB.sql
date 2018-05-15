
/*create table*/

DROP TABLE IF EXISTS `ADMINS`;
DROP TABLE IF EXISTS `CASE_BASE`;
DROP TABLE IF EXISTS `CASES_TO_BE_VALIDATED`;
DROP TABLE IF EXISTS `ORIGIN`;

CREATE TABLE IF NOT EXISTS ADMINS(
	idAdmin int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	password varchar(30) DEFAULT NULL,
	firstname varchar(30) DEFAULT NULL,
	lastname varchar(30) DEFAULT NULL,
	email varchar(30) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
		
CREATE TABLE IF NOT EXISTS ORIGIN(
	idOrigin int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	originSource varchar(200) CHARACTER SET utf8,
	note varchar(200) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;

CREATE TABLE IF NOT EXISTS CASE_BASE (
	idBaseCase int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	problem varchar (200) CHARACTER SET utf8,
	solution varchar(200) CHARACTER SET utf8,
	status varchar(200) CHARACTER SET utf8,
	erreur varchar(200) CHARACTER SET utf8,
	correction varchar(200) CHARACTER SET utf8,
	erreurIndex varchar(200) CHARACTER SET utf8,
	idProvenance int NOT NULL ,
	lang varchar(10) CHARACTER SET utf8,
	
CONSTRAINT fk__provenance FOREIGN KEY (idProvenance) REFERENCES ORIGIN(idOrigin)) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS CASES_TO_BE_VALIDATED (
	idValidated int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	problem_to_be_validated varchar (200) CHARACTER SET utf8,
	solution_to_be_validated varchar(200) CHARACTER SET utf8,
	status varchar(200) CHARACTER SET utf8,
	erreur varchar(200) CHARACTER SET utf8,
	correction varchar(200) CHARACTER SET utf8,
	erreurIndex varchar(200) CHARACTER SET utf8,
	idProvenance_to_be_validated int NOT NULL ,
	lang_to_be_validated varchar(10) CHARACTER SET utf8,
	
CONSTRAINT fk__provenance_to_be_validated FOREIGN KEY (idProvenance_to_be_validated) REFERENCES ORIGIN(idOrigin)) ENGINE=InnoDB DEFAULT CHARSET=utf8;