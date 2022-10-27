-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema forum_system_api
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum_system_api
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_system_api` DEFAULT CHARACTER SET latin1 ;
USE `forum_system_api` ;

-- -----------------------------------------------------
-- Table `forum_system_api`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_api`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `locked` TINYINT(4) NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_system_api`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_api`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(128) NOT NULL,
  `password` VARCHAR(256) NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `password_UNIQUE` (`password` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_system_api`.`conversations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_api`.`conversations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `sender_id` INT(11) NOT NULL,
  `recipient_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_users_users2_idx` (`recipient_id` ASC) VISIBLE,
  INDEX `fk_users_has_users_users1_idx` (`sender_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_users_users1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_system_api`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_users_users2`
    FOREIGN KEY (`recipient_id`)
    REFERENCES `forum_system_api`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_system_api`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_api`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(512) NOT NULL,
  `datestamp` DATETIME NOT NULL,
  `user_id` INT(11) NOT NULL,
  `conversation_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_messages_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_messages_conversations1_idx` (`conversation_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_api`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_conversations1`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `forum_system_api`.`conversations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_system_api`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_api`.`topics` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(256) NOT NULL,
  `datestamp` DATETIME NOT NULL,
  `locked` TINYINT(4) NULL DEFAULT 0,
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_topics_categories_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_system_api`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_api`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_system_api`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_api`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(1024) NOT NULL,
  `datestamp` DATETIME NOT NULL,
  `upvotes` INT(11) NULL DEFAULT NULL,
  `downvotes` INT(11) NULL DEFAULT NULL,
  `best_reply` TINYINT(4) NULL DEFAULT 0,
  `topic_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_replies_topics1_idx` (`topic_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum_system_api`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_api`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_system_api`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_system_api`.`votes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `reply_id` INT(11) NOT NULL,
  `vote` TINYINT(4) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_replies_replies1_idx` (`reply_id` ASC) VISIBLE,
  INDEX `fk_users_has_replies_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_votes_replies1`
    FOREIGN KEY (`reply_id`)
    REFERENCES `forum_system_api`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_votes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_system_api`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
