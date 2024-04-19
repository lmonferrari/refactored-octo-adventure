CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    weight DECIMAL(10, 2) NOT NULL,
    packing VARCHAR(255) NOT NULL
);

INSERT INTO products (name, weight, packing) VALUES 
('Smartphone', 212, 'Caixa de Papelão'),
('Tablet', 215, 'Caixa de Papelão'),
('Tablet', 890, 'Plástico Bolha'),
('Tablet', 700, 'Plástico Bolha'),
('Smartphone', 230, 'Caixa de Papelão'),
('Smartphone', 240, 'Caixa de Papelão'),
('Tablet', 730, 'Plástico Bolha'),
('Smartphone', 780, 'Plástico Bolha'),
('Smartphone', 218, 'Caixa de Papelão'),
('Tablet', 750, 'Plástico Bolha'),
('Smartphone', 202, 'Caixa de Papelão'),
('Tablet', 680, 'Plástico Bolha');
