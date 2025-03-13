-- SQLite3 Script

-- -----------------------------------------------------
-- Schema EBilling_System
-- -----------------------------------------------------

-- SQLite does not support CREATE SCHEMA, so we skip this part
-- CREATE SCHEMA IF NOT EXISTS `EBilling_System` DEFAULT CHARACTER SET utf8 ;
-- USE `EBilling_System` ;

-- -----------------------------------------------------
-- Table `producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `producto` (
  `id_producto` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL
  `descripcion` TEXT NOT NULL,
  `precio` INTEGER NOT NULL);

-- -----------------------------------------------------
-- Table `cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cliente` (
  `id_cliente` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre_cliente` TEXT NOT NULL);

-- -----------------------------------------------------
-- Table `usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` TEXT NOT NULL,
  `email` TEXT NOT NULL,
  `password` TEXT NOT NULL,
  `tiempo_creado` TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- -----------------------------------------------------
-- Table `facturas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facturas` (
  `id_factura` INTEGER PRIMARY KEY AUTOINCREMENT,
  `numero_factura` INTEGER NOT NULL,
  `fecha_emision` DATE NOT NULL,
  `hora_emision` TIME NOT NULL,
  `id_cliente` INTEGER NOT NULL,
  `id_producto` INTEGER NOT NULL,
  `comprobante` BLOB NOT NULL,
  `emisor` INTEGER NOT NULL,
  `subtotal` INTEGER NOT NULL,
  `iva` INTEGER NOT NULL,
  `total` INTEGER NOT NULL,
  FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`),
  FOREIGN KEY (`emisor`) REFERENCES `usuario` (`id`));

-- SQLite does not support setting SQL modes or foreign key checks
-- SET SQL_MODE=@OLD_SQL_MODE;
-- SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
-- SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
