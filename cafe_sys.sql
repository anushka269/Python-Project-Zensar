-- 1. Create Tables

-- MenuItems Table
CREATE TABLE MenuItems (
    ItemID INT PRIMARY KEY AUTO_INCREMENT,
    ItemName VARCHAR(100) NOT NULL,
    Category VARCHAR(50),
    Price DECIMAL(10, 2),
    PopularityScore INT DEFAULT 0
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    ItemID INT,
    Quantity INT,
    OrderDate DATE,
    FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID)
);

-- Inventory Table
CREATE TABLE Inventory (
    ItemID INT PRIMARY KEY,
    StockQuantity INT,
    FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID)
);

-- Staff Table
CREATE TABLE Staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Role VARCHAR(50)
);

-- StaffSchedule Table
CREATE TABLE StaffSchedule (
    ScheduleID INT PRIMARY KEY AUTO_INCREMENT,
    StaffID INT,
    ShiftDate DATE,
    ShiftTime VARCHAR(20),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);


-- 2. Insert Sample Data

-- MenuItems Data
INSERT INTO MenuItems (ItemName, Category, Price, PopularityScore) VALUES
('Espresso', 'Beverage', 150.00, 85),
('Cappuccino', 'Beverage', 200.00, 90),
('Cheesecake', 'Dessert', 250.00, 75),
('Veg Sandwich', 'Snack', 180.00, 70),
('Chocolate Brownie', 'Dessert', 220.00, 95);

-- Orders Data
INSERT INTO Orders (ItemID, Quantity, OrderDate) VALUES
(1, 2, '2025-01-09'),
(2, 1, '2025-01-09'),
(3, 3, '2025-01-10'),
(5, 2, '2025-01-10');

-- Inventory Data
INSERT INTO Inventory (ItemID, StockQuantity) VALUES
(1, 50),
(2, 40),
(3, 20),
(4, 30),
(5, 15);

-- Staff Data
INSERT INTO Staff (Name, Role) VALUES
('Alice Johnson', 'Barista'),
('Bob Smith', 'Chef'),
('Carol White', 'Waiter');

-- StaffSchedule Data
INSERT INTO StaffSchedule (StaffID, ShiftDate, ShiftTime) VALUES
(1, '2025-01-10', '09:00-17:00'),
(2, '2025-01-10', '10:00-18:00'),
(3, '2025-01-10', '12:00-20:00');
