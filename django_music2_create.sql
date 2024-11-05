-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema django_music2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema django_music2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `django_music2` DEFAULT CHARACTER SET utf8mb4 ;
USE `django_music2` ;

-- -----------------------------------------------------
-- Table `django_music2`.`media_format`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`media_format` (
  `id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`label`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`label` (
  `id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`manufacturer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`manufacturer` (
  `id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`album`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`album` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `catalog_number` VARCHAR(15) NULL,
  `name_original` VARCHAR(100) NULL,
  `name_romaji` VARCHAR(100) NULL,
  `name_english` VARCHAR(160) NULL,
  `count_of_discs` TINYINT UNSIGNED NOT NULL,
  `count_of_tracks` INT UNSIGNED NOT NULL,
  `media_format` TINYINT UNSIGNED NOT NULL,
  `label` TINYINT UNSIGNED NULL,
  `manufacturer` TINYINT UNSIGNED NULL,
  `notes` VARCHAR(380) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `ID_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_album_media_format_idx` (`media_format` ASC) INVISIBLE,
  INDEX `fk_album_label_idx` (`label` ASC) VISIBLE,
  INDEX `fk_album_manufacturer_idx` (`manufacturer` ASC) VISIBLE,
  CONSTRAINT `fk_album_media_format`
    FOREIGN KEY (`media_format`)
    REFERENCES `django_music2`.`media_format` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_album_label`
    FOREIGN KEY (`label`)
    REFERENCES `django_music2`.`label` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_album_manufacturer`
    FOREIGN KEY (`manufacturer`)
    REFERENCES `django_music2`.`manufacturer` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`track`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`track` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name_original` VARCHAR(100) NULL,
  `name_romaji` VARCHAR(100) NULL,
  `name_english` VARCHAR(160) NULL,
  `album` INT UNSIGNED NOT NULL,
  `number_in_album` INT NOT NULL,
  `duration` TIME NOT NULL,
  `notes` VARCHAR(380) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_track_album1_idx` (`album` ASC) VISIBLE,
  CONSTRAINT `fk_track_album`
    FOREIGN KEY (`album`)
    REFERENCES `django_music2`.`album` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`ost_from`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`ost_from` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name_original` VARCHAR(100) NULL,
  `name_romaji` VARCHAR(100) NULL,
  `name_english` VARCHAR(160) NULL,
  `date` DATE NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`author`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`author` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name_original` VARCHAR(60) NOT NULL,
  `name_romaji` VARCHAR(65) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`track_ost_from`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`track_ost_from` (
  `track_id` INT UNSIGNED NOT NULL,
  `ost_from_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`track_id`, `ost_from_id`),
  INDEX `fk_track_ost_from_ost_from_idx` (`ost_from_id` ASC) VISIBLE,
  INDEX `fk_track_ost_from_track_idx` (`track_id` ASC) VISIBLE,
  CONSTRAINT `fk_track_ost_from_track`
    FOREIGN KEY (`track_id`)
    REFERENCES `django_music2`.`track` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_track_ost_from_ost_from`
    FOREIGN KEY (`ost_from_id`)
    REFERENCES `django_music2`.`ost_from` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`performer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`performer` (
  `track_id` INT UNSIGNED NOT NULL,
  `author_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`track_id`, `author_id`),
  INDEX `fk_performer_author_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_performer_track_idx` (`track_id` ASC) INVISIBLE,
  CONSTRAINT `fk_performer_track`
    FOREIGN KEY (`track_id`)
    REFERENCES `django_music2`.`track` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_performer_author`
    FOREIGN KEY (`author_id`)
    REFERENCES `django_music2`.`author` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`lyricist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`lyricist` (
  `track_id` INT UNSIGNED NOT NULL,
  `author_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`track_id`, `author_id`),
  INDEX `fk_lyricist_author_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_lyricist_track_idx` (`track_id` ASC) VISIBLE,
  CONSTRAINT `fk_lyricist_track`
    FOREIGN KEY (`track_id`)
    REFERENCES `django_music2`.`track` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_lyricist_author`
    FOREIGN KEY (`author_id`)
    REFERENCES `django_music2`.`author` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`composer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`composer` (
  `track_id` INT UNSIGNED NOT NULL,
  `author_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`track_id`, `author_id`),
  INDEX `fk_composer_author_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_composer_track_idx` (`track_id` ASC) VISIBLE,
  CONSTRAINT `fk_composer_track`
    FOREIGN KEY (`track_id`)
    REFERENCES `django_music2`.`track` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_composer_author`
    FOREIGN KEY (`author_id`)
    REFERENCES `django_music2`.`author` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `django_music2`.`arranger`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_music2`.`arranger` (
  `track_id` INT UNSIGNED NOT NULL,
  `author_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`track_id`, `author_id`),
  INDEX `fk_arranger_author_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_arranger_track_idx` (`track_id` ASC) VISIBLE,
  CONSTRAINT `fk_arranger_track`
    FOREIGN KEY (`track_id`)
    REFERENCES `django_music2`.`track` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_arranger_author`
    FOREIGN KEY (`author_id`)
    REFERENCES `django_music2`.`author` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
