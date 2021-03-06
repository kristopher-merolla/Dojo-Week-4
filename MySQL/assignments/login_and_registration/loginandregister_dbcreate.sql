-- MySQL Script generated by MySQL Workbench
-- Wed May 17 22:20:29 2017
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema loginandregisterdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema loginandregisterdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `loginandregisterdb` DEFAULT CHARACTER SET utf8 ;
USE `loginandregisterdb` ;

-- -----------------------------------------------------
-- Table `loginandregisterdb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loginandregisterdb`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `salt` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
