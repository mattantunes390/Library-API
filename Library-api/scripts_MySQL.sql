CREATE SCHEMA `library`;
CREATE TABLE `library`.`books` (
  `idbook` INT(11) NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(50) NULL DEFAULT NULL,
  `autor` VARCHAR(50) NULL DEFAULT NULL,
  `ano_publicacao` INT(11) NULL DEFAULT NULL,
  `preco_locacao` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idbook`),
  UNIQUE INDEX `UNIQUE` (`titulo` ASC, `autor` ASC, `ano_publicacao` ASC));
CREATE TABLE `library`.`clients` (
  `idclient` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idclient`));
CREATE TABLE `library`.`reservas` (
  `idreserva` INT(11) NOT NULL AUTO_INCREMENT,
  `data_reserva` DATETIME NOT NULL,
  `data_entrega` DATETIME NOT NULL,
  `id_book` INT(11) NOT NULL,
  `id_client` INT(11) NOT NULL,
  PRIMARY KEY (`idreserva`),
  INDEX `fk_books_idx` (`id_book` ASC),
  INDEX `fk_clients_idx` (`id_client` ASC),
  CONSTRAINT `fk_books`
    FOREIGN KEY (`id_book`)
    REFERENCES `library`.`books` (`idbook`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_clients`
    FOREIGN KEY (`id_client`)
    REFERENCES `library`.`clients` (`idclient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
