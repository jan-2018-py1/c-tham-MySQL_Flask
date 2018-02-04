-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema 0loginregistration
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema 0loginregistration
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `0loginregistration` DEFAULT CHARACTER SET utf8 ;
USE `0loginregistration` ;

-- -----------------------------------------------------
-- Table `0loginregistration`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `0loginregistration`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email_address` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `dob` DATETIME NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
