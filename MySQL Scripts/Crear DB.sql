-- Crear esquema
CREATE SCHEMA reto2_talento_b DEFAULT CHARACTER SET UTF8MB4;
USE reto2_talento_b;

-- Tabla Titulares
CREATE TABLE reto2_talento_b.titulares (
  id_titular INT UNSIGNED NOT NULL AUTO_INCREMENT,
  documento_identidad BIGINT NOT NULL,
  tipo_documento ENUM("CC", "TI", "CE") NOT NULL,
  nombres VARCHAR(100) NOT NULL,
  apellidos VARCHAR(100) NOT NULL,
  PRIMARY KEY (id_titular),
  UNIQUE INDEX idx_documento_identidad_tipo_documento (documento_identidad ASC, tipo_documento ASC) VISIBLE
);
  
-- Tabla Cuentas
CREATE TABLE reto2_talento_b.cuentas (
  numero_cuenta BIGINT UNSIGNED NOT NULL,
  password VARCHAR(50) NOT NULL,
  tipo_cuenta ENUM("Ahorros", "Corriente", "Nómina") NOT NULL,
  saldo DOUBLE NOT NULL,
  id_titular INT UNSIGNED NOT NULL,
  PRIMARY KEY (numero_cuenta),
  INDEX fk_cuentas_titulares1_idx (id_titular ASC) VISIBLE,
  CONSTRAINT fk_cuentas_titulares1
    FOREIGN KEY (id_titular)
    REFERENCES titulares (id_titular)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Tabla Tipo de Transacción    
CREATE TABLE reto2_talento_b.tipo_transaccion (
  id_tipo_transaccion INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre_transaccion VARCHAR(100) NOT NULL,
  descripcion TEXT NOT NULL,
  PRIMARY KEY (id_tipo_transaccion)
);
  
-- Tabla Movimientos
CREATE TABLE reto2_talento_b.movimientos (
	id_movimiento INT UNSIGNED NOT NULL AUTO_INCREMENT,
    valor DOUBLE NOT NULL,
    fecha_transaccion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    numero_cuenta_salida BIGINT UNSIGNED NOT NULL,
    numero_cuenta_entrada BIGINT UNSIGNED NULL,
    id_tipo_transaccion INT UNSIGNED NOT NULL,
    PRIMARY KEY (id_movimiento),
    INDEX fk_movimientos_cuentas_idx (numero_cuenta_salida ASC) VISIBLE,
    INDEX fk_movimientos_cuentas1_idx (numero_cuenta_entrada ASC) VISIBLE,
	INDEX fk_movimientos_tipo_transaccion1_idx (id_tipo_transaccion ASC) VISIBLE,
    CONSTRAINT fk_movimientos_cuentas
		FOREIGN KEY (numero_cuenta_salida)
        REFERENCES cuentas (numero_cuenta)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_movimientos_cuentas1
		FOREIGN KEY (numero_cuenta_entrada)
		REFERENCES cuentas (numero_cuenta)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT fk_movimientos_tipo_transaccion1
		FOREIGN KEY (id_tipo_transaccion)
		REFERENCES tipo_transaccion (id_tipo_transaccion)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

DELIMITER $$
CREATE TRIGGER sumar_saldo_cuenta_entrada
AFTER INSERT ON movimientos
FOR EACH ROW
BEGIN
	IF NEW.numero_cuenta_entrada IS NOT NULL THEN
		UPDATE cuentas
        SET saldo = saldo + NEW.valor
		WHERE numero_cuenta = NEW.numero_cuenta_entrada;
    END IF;
END;
$$

$$
CREATE TRIGGER restar_saldo_cuenta_salida
AFTER INSERT ON movimientos
FOR EACH ROW
BEGIN
	UPDATE cuentas
    SET saldo = saldo - NEW.valor
    WHERE numero_cuenta = NEW.numero_cuenta_salida;
END;
$$    

DELIMITER ;