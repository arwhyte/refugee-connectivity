-- python run_mysql_script.py  -c config/refconn.yaml -p data/sql/refugee_create.sql
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema refugee
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema refugee
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `refugee` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `refugee` ;

-- -----------------------------------------------------
-- Table `refugee`.`camp_admin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `refugee`.`camp_admin` ;

CREATE TABLE IF NOT EXISTS camp_admin
  (
    camp_admin_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    camp_admin_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (camp_admin_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO camp_admin (camp_admin_name) VALUES
  ('Military'), ('Local Government'), ('National Government - Immigration'), ('National Government - Non-Immigration');

-- -----------------------------------------------------
-- Table `refugee`.`country`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `refugee`.`country` ;

CREATE TABLE IF NOT EXISTS `refugee`.`country` (
  `country_id` INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `country_name` VARCHAR(45) NOT NULL UNIQUE,
  PRIMARY KEY (`country_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO country (country_name) VALUES
  ('Greece'), ('Serbia');

-- -----------------------------------------------------
-- Table `refugee`.`camp_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `refugee`.`camp_type` ;

CREATE TABLE IF NOT EXISTS camp_type (
  camp_type_id INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
  camp_type_name VARCHAR(45) NOT NULL UNIQUE,
  country_id INT NOT NULL,
  PRIMARY KEY (camp_type_id),
  FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE RESTRICT ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- Set FK variables and populate the sub_region table.
SET @fk_greece =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Greece'
  );
SET @fk_serbia =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Serbia'
  );

INSERT IGNORE INTO camp_type (camp_type_name, country_id) VALUES
  ('TAS', @fk_greece),
  ('RIC', @fk_greece),
  ('RC', @fk_greece),
  ('TC', @fk_serbia),
  ('AC', @fk_serbia);

-- -----------------------------------------------------
-- Table `refugee`.`camp`
-- -----------------------------------------------------
CREATE TEMPORARY TABLE temp_camp
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    camp_name VARCHAR(45) NOT NULL UNIQUE,
    camp_file_name VARCHAR(45) NOT NULL UNIQUE,
    country VARCHAR(45) NOT NULL,
    camp_admin VARCHAR(45) NULL,
    camp_type VARCHAR(45) NULL,
    longitude FLOAT NULL,
    -- longitude DECIMAL(11, 8) NOT NULL,
    latitude FLOAT NULL,
    -- latitude DECIMAL(10, 8) NOT NULL,
    bandwidth_up FLOAT NULL,
    bandwidth_down FLOAT NULL,
    -- area_hectares FLOAT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load UNESCO data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/user/Desktop/si664/refugee-connectivity/data/csv/camp.csv'
INTO TABLE temp_camp
  -- CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  -- ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, camp_name, camp_file_name, camp_type, @dummy, longitude,latitude, bandwidth_down, bandwidth_up, country, camp_admin);

DROP TABLE IF EXISTS `refugee`.`camp` ;

CREATE TABLE IF NOT EXISTS `refugee`.`camp` (
  `camp_id` INT(11) NOT NULL AUTO_INCREMENT,
  `camp_name` VARCHAR(45) NOT NULL,
  `camp_file_name` VARCHAR(45) NOT NULL,
  `country_id` INT(11) NULL DEFAULT NULL,
  `camp_admin_id` INT(11) NULL,
  `camp_type_id` INT(11) NULL DEFAULT NULL,
  `latitude` FLOAT NOT NULL,
  `longitude` FLOAT NOT NULL,
  `bandwidth_up` FLOAT NULL,
  `bandwidth_down` FLOAT NULL,
  PRIMARY KEY (`camp_id`),
  UNIQUE INDEX `camp_id_UNIQUE` (`camp_id` ASC) VISIBLE,
  UNIQUE INDEX `camp_name_UNIQUE` (`camp_name` ASC) VISIBLE,
  INDEX `country_id_idx` (`country_id` ASC) VISIBLE,
  INDEX `camp_admin_id_idx` (`camp_admin_id` ASC) VISIBLE,
  INDEX `camp_type_id_idx` (`camp_type_id` ASC) VISIBLE,
  CONSTRAINT `camp_admin_id`
    FOREIGN KEY (`camp_admin_id`)
    REFERENCES `refugee`.`camp_admin` (`camp_admin_id`),
  CONSTRAINT `camp_type_id`
    FOREIGN KEY (`camp_type_id`)
    REFERENCES `refugee`.`camp_type` (`camp_type_id`),
  CONSTRAINT `country_id`
    FOREIGN KEY (`country_id`)
    REFERENCES `refugee`.`country` (`country_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO camp (camp_name, camp_file_name, country_id, camp_admin_id, camp_type_id,longitude, latitude, bandwidth_up, bandwidth_down)
SELECT tc.camp_name, tc.camp_file_name,country.country_id,ca.camp_admin_id,ct.camp_type_id,tc.longitude,tc.latitude,
       tc.bandwidth_up, tc.bandwidth_down
  FROM temp_camp tc
       LEFT JOIN country
              ON tc.country = country.country_name
       LEFT JOIN camp_admin ca
              ON tc.camp_admin like concat('%',ca.camp_admin_name,'%')
       LEFT JOIN camp_type ct
              ON tc.camp_type = ct.camp_type_name
 ORDER BY tc.id;

 DROP TEMPORARY TABLE temp_camp;

-- -----------------------------------------------------
-- Table `refugee`.`monthly_usage_per_camp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS temp_mupc;

CREATE TEMPORARY TABLE temp_mupc
  (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    camp VARCHAR(45) NOT NULL,
    total_infrastructure_devices INTEGER NOT NULL,
    cmy VARCHAR(100) NOT NULL UNIQUE,
    month INT NOT NULL, 
    year INT NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load UNESCO data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/user/Desktop/si664/refugee-connectivity/data/csv/monthly_usage_per_camp.csv'
INTO TABLE temp_mupc
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  -- ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, camp, @dummy, total_infrastructure_devices, cmy, month, year);

DROP TABLE IF EXISTS `refugee`.`monthly_usage_per_camp` ;

CREATE TABLE IF NOT EXISTS `refugee`.`monthly_usage_per_camp` (
  `mupc_id` INT(11) NOT NULL AUTO_INCREMENT,
  `camp_id` INT(11) NOT NULL,
  `total_infrastructure_devices` INT(11) NOT NULL,
  `cmy` VARCHAR(100) NULL DEFAULT NULL,
  `month_num` INT NULL,
  `year_num` INT NULL,
  PRIMARY KEY (`mupc_id`),
  UNIQUE INDEX `mupc_id_UNIQUE` (`mupc_id` ASC) VISIBLE,
  INDEX `camp_id_idx` (`camp_id` ASC) VISIBLE,
  CONSTRAINT `camp_id`
    FOREIGN KEY (`camp_id`)
    REFERENCES `refugee`.`camp` (`camp_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO monthly_usage_per_camp (camp_id, total_infrastructure_devices, cmy, month_num, year_num)
SELECT camp.camp_id, tm.total_infrastructure_devices,tm.cmy,tm.month,tm.year
  FROM temp_mupc tm
       LEFT JOIN camp
              ON tm.camp = camp.camp_file_name
 ORDER BY tm.id;

 -- DROP TEMPORARY TABLE temp_mupc;

-- -----------------------------------------------------
-- Table `refugee`.`application_category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `refugee`.`application_category` ;

CREATE TABLE IF NOT EXISTS `refugee`.`application_category` (
  `application_category_id` INT(11) NOT NULL AUTO_INCREMENT,
  `application_category_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`application_category_id`),
  UNIQUE INDEX `application_category_id_UNIQUE` (`application_category_id` ASC) VISIBLE,
  UNIQUE INDEX `application_category_name_UNIQUE` (`application_category_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO application_category (application_category_name) VALUES
  ('Video'), ('Other'), ('Social web'), ('Music'), ('Email'), ('Advertising'),('Software & anti-virus updates'), 
  ('Productivity'), ('File sharing'), ('Blogging'), ('VoIP & video conferencing'), ('Photo sharing'), ('News'), ('P2P'), 
  ('Gaming'), ('Online backup'), ('Sports'), ('Remote monitoring & management'), ('Security'), ('Web file sharing'),
  ('Business management'), ('Web payments'), ('Cloud services'), ('Electronic health records');

-- -----------------------------------------------------
-- Table `refugee`.`application_usage`
-- -----------------------------------------------------
CREATE TEMPORARY TABLE temp_appu
  (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    cmy VARCHAR(100) NOT NULL,
    application_category VARCHAR(45) NOT NULL,
    total_usage_kB FLOAT NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load UNESCO data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/user/Desktop/si664/refugee-connectivity/data/csv/application_usage.csv'
INTO TABLE temp_appu
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  -- ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, @dummy, @dummy, application_category, total_usage_kB, @dummy, cmy);

DROP TABLE IF EXISTS `refugee`.`application_usage` ;

CREATE TABLE IF NOT EXISTS `refugee`.`application_usage` (
  `appu_id` INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `mupc_id` INT(11) NOT NULL,
  `application_category_id` INT(11) NULL DEFAULT NULL,
  `total_usage_kB` FLOAT NULL DEFAULT NULL,
    PRIMARY KEY (`appu_id`),
  CONSTRAINT `application_category_id`
    FOREIGN KEY (`application_category_id`)
    REFERENCES `refugee`.`application_category` (`application_category_id`),
  CONSTRAINT `mupc_id`
    FOREIGN KEY (`mupc_id`)
    REFERENCES `refugee`.`monthly_usage_per_camp` (`mupc_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO application_usage (mupc_id, application_category_id, total_usage_kB)
SELECT mupc.mupc_id, ac.application_category_id, ta.total_usage_kB
  FROM temp_appu ta
       LEFT JOIN monthly_usage_per_camp mupc
              ON ta.cmy like concat('%',mupc.cmy,'%')
       LEFT JOIN application_category ac
              ON ta.application_category = ac.application_category_name
 ORDER BY ta.id;

 DROP TEMPORARY TABLE temp_appu;

-- -----------------------------------------------------
-- Table `refugee`.`camp_demographics`
-- -----------------------------------------------------
DROP TABLE IF EXISTS temp_camp_dem;

CREATE TEMPORARY TABLE temp_camp_dem
  (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    cmy VARCHAR(100) NOT NULL,
    camp_population INT NULL DEFAULT NULL,
    camp_capacity INT NULL DEFAULT NULL,
    overcapacity BINARY NULL DEFAULT NULL,
    adultmale FLOAT NULL DEFAULT NULL,
    adultfemale FLOAT NULL DEFAULT NULL,
    children FLOAT NULL DEFAULT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load UNESCO data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/user/Desktop/si664/refugee-connectivity/data/csv/camp_demographics.csv'
INTO TABLE temp_camp_dem
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  -- ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, @dummy, @dummy, @dummy, camp_population, camp_capacity, overcapacity,adultmale,adultfemale,children,@dummy,cmy);

DROP TABLE IF EXISTS `refugee`.`camp_demographics` ;

CREATE TABLE IF NOT EXISTS `refugee`.`camp_demographics` (
  `camp_dem_id` INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `mupc_id` INT(11) NOT NULL,
  `camp_population` INT(11) NULL DEFAULT NULL,
  `camp_capacity` FLOAT NULL DEFAULT NULL,
  `adultmale` FLOAT NULL DEFAULT NULL,
  `adultfemale` FLOAT NULL DEFAULT NULL,
  `children` FLOAT NULL DEFAULT NULL,
  `overcapacity` BINARY NOT NULL,
  PRIMARY KEY(camp_dem_id),
  CONSTRAINT `camp_demographics_ibfk_1`
    FOREIGN KEY (`mupc_id`)
    REFERENCES `refugee`.`monthly_usage_per_camp` (`mupc_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO camp_demographics
  (mupc_id,camp_population,camp_capacity,adultmale,adultfemale,children,overcapacity)
SELECT mupc.mupc_id, tcd.camp_population,tcd.camp_capacity,tcd.adultmale,tcd.adultfemale,tcd.children,tcd.overcapacity
  FROM temp_camp_dem tcd
       LEFT JOIN monthly_usage_per_camp mupc
              ON tcd.cmy like concat('%',mupc.cmy,'%')
 ORDER BY tcd.id;

UPDATE camp_demographics
set camp_capacity = null where camp_capacity = 0;

DROP TEMPORARY TABLE temp_camp_dem;
-- -----------------------------------------------------
-- Table `refugee`.`daily_usage_per_camp`
-- -----------------------------------------------------
CREATE TEMPORARY TABLE temp_dupc
  (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    cmy VARCHAR(100) NOT NULL,
    date_field VARCHAR(45) NOT NULL,
    total_clients INT NULL DEFAULT NULL,
    dupc VARCHAR(45) NOT NULL,
    total_usage_kB FLOAT NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load UNESCO data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/user/Desktop/si664/refugee-connectivity/data/csv/daily_usage_per_camp.csv'
INTO TABLE temp_dupc
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  -- ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, @dummy, @dummy, @the_date, total_clients, cmy, dupc, total_usage_kB)
	SET date_field = str_to_date(@the_date,'%m/%d/%Y');

DROP TABLE IF EXISTS `refugee`.`daily_usage_per_camp` ;

CREATE TABLE IF NOT EXISTS `refugee`.`daily_usage_per_camp` (
  `dupc_id` INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `mupc_id` INT(11) NULL,
  `date_field` DATE NULL,
  `total_clients` INT(11) NULL,
  `total_usage_kB` FLOAT NULL,
  `dupc` VARCHAR(45) NOT NULL UNIQUE,
  PRIMARY KEY (`dupc_id`),
  UNIQUE INDEX `dupc_id_UNIQUE` (`dupc_id` ASC) VISIBLE,
  INDEX `mupc_id` (`mupc_id` ASC) VISIBLE,
  CONSTRAINT `daily_usage_per_camp_ibfk_1`
    FOREIGN KEY (`mupc_id`)
    REFERENCES `refugee`.`monthly_usage_per_camp` (`mupc_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO daily_usage_per_camp
  (mupc_id,date_field,total_clients,total_usage_kB,dupc)
SELECT mupc.mupc_id, td.date_field, td.total_clients,td.total_usage_kB,td.dupc
  FROM temp_dupc td
       LEFT JOIN monthly_usage_per_camp mupc
              ON td.cmy = mupc.cmy
 ORDER BY td.id;

DROP TEMPORARY TABLE temp_dupc;

update daily_usage_per_camp set total_clients = null 
where (total_clients=0) and (total_usage_kB>0);


-- -----------------------------------------------------
-- Table `refugee`.`nationality`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `refugee`.`nationality` ;

CREATE TABLE IF NOT EXISTS `refugee`.`nationality` (
  `nationality_id` INT(11) NOT NULL AUTO_INCREMENT,
  `nationality_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`nationality_id`),
  UNIQUE INDEX `nationality_id_UNIQUE` (`nationality_id` ASC) VISIBLE,
  UNIQUE INDEX `nationality_name_UNIQUE` (`nationality_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO nationality (nationality_name) VALUES
  ('Syrian'), ('Iraqi'), ('Pakistani'), ('Palestinian'), ('Iranian'), ('Afghan'), ('Yemeni'), ('Stateless'), 
  ('Congolese'), ('Eritrean'), ('Somali'), ('Kuwaiti'), ('Moroccan'), ('Egyptian'), ('Algerian');


-- -----------------------------------------------------
-- Table `refugee`.`refugee_nationality`
-- -----------------------------------------------------
CREATE TEMPORARY TABLE temp_ref_nation
  (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    cmy VARCHAR(100) NOT NULL,
    nationality VARCHAR(45) NOT NULL,
    nationality_proportion FLOAT NULL DEFAULT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/user/Desktop/si664/refugee-connectivity/data/csv/refugee_nationality.csv'
INTO TABLE temp_ref_nation
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  -- ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, @dummy, @dummy, nationality, nationality_proportion, cmy);

DROP TABLE IF EXISTS `refugee`.`refugee_nationality` ;

CREATE TABLE IF NOT EXISTS `refugee`.`refugee_nationality` (
  `ref_nat_id` INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `mupc_id` INT(11) NOT NULL,
  `nationality_id` INT(11) NOT NULL,
  `nationality_proportion` FLOAT NOT NULL,
  INDEX `mupc_id_idx` (`mupc_id` ASC) VISIBLE,
  INDEX `nationality_id_idx` (`nationality_id` ASC) VISIBLE,
  PRIMARY KEY(ref_nat_id),
  CONSTRAINT `nationality_id`
    FOREIGN KEY (`nationality_id`)
    REFERENCES `refugee`.`nationality` (`nationality_id`),
  CONSTRAINT `refugee_nationality_ibfk_1`
    FOREIGN KEY (`mupc_id`)
    REFERENCES `refugee`.`monthly_usage_per_camp` (`mupc_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT IGNORE INTO refugee_nationality
  (mupc_id, nationality_id, nationality_proportion)
SELECT mupc.mupc_id, na.nationality_id, trn.nationality_proportion
  FROM temp_ref_nation trn 
       LEFT JOIN monthly_usage_per_camp mupc
              ON trn.cmy like concat('%',mupc.cmy,'%')
       LEFT JOIN nationality na
              ON na.nationality_name = trn.nationality
 ORDER BY trn.id;

DROP TEMPORARY TABLE temp_ref_nation;

-- dropping unnecessary columns

ALTER TABLE daily_usage_per_camp DROP COLUMN dupc;
ALTER TABLE camp DROP COLUMN camp_file_name;
ALTER TABLE monthly_usage_per_camp DROP COLUMN cmy;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
