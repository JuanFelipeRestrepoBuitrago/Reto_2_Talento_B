USE reto2_talento_b;

-- Insertar titulares
INSERT INTO titulares (documento_identidad, tipo_documento, nombres, apellidos)
VALUES (1027740136, 'CC', 'Juan Felipe', 'Restrepo Buitrago'), (1027740136, 'TI', 'Juan Felipe', 'Restrepo Buitrago'), (98666926, 'CC', 'Juan Manuel', 'Idarraga Restrepo'),
	   (1034988369, 'TI', 'Santiago', 'Celis Loaiza'), (1045975362, 'CE', 'Pedro', 'Gutierrez Guzmán'), (1065231754, 'TI', 'Manuela', 'Campo Gómez'),
       (1045987256, 'CE', 'Carolina', 'Ramírez Londoño'), (1065234571, 'CC', 'Ana María', 'Mesa Toro');
       
-- Insertar cuentas
INSERT INTO cuentas (numero_cuenta, password, tipo_cuenta, saldo, id_titular)
VALUES (1034598672, 'Felipe123', 'Nómina', 14250550.2, 1), (5236487596, 'Pipe123', 'Ahorros', 500000.0, 2), (3215649875, 'Juan123', 'Corriente', 5200000.65, 3),
	   (7896542318, 'Felipe123', 'Corriente', 2500652.364, 1), (5124789563, 'Santi123', 'Ahorros', 65320.63, 4), (4125638759, 'Pedro123', 'Nómina', 3000000.0, 5),
       (1236548962, 'Manu123', 'Ahorros', 250.3, 6), (2365214896, 'Caro123','Corriente', 12563300.0, 7), (5469857452, 'Ana123','Nómina', 86000000.0, 8);

-- Insertar tipo de transacción
INSERT INTO tipo_transaccion (nombre_transaccion, descripcion)
VALUES ("Transacción a crédito", "Es decir, una transacción en la que el pago no es inmediato. En otras palabras, no se realiza desembolso al recibir el bien o el servicio."),
	   ("Transacción en efectivo", "Es decir, una transacción en la que, al recibir la propiedad sobre el bien o el servicio, a su vez, se realiza el desembolso correspondiente."),
       ("Transacción externa", "Cuando la empresa realiza transacciones comerciales con individuos externos a la propia compañía. Es decir, cuando una empresa comercia con agentes externos."),
       ("Transacción interna", "Muy habituales. Cuando una empresa registra transacciones sin interactuar con agentes externos. Es decir, aquellas transacciones que, como la amortización o depreciación de activos, no involucran a otras partes.");
       
-- Insertar movimientos
INSERT INTO movimientos (valor, numero_cuenta_salida, numero_cuenta_entrada, id_tipo_transaccion)
VALUES (100000.0, 4125638759, 1236548962, 1);
-- Cuenta 4125638759 del titular 5 termina con saldo 2900000.0 y cuenta 1236548962 del titular 6 termina con saldo 100250.3
       
SELECT * 
FROM cuentas;       