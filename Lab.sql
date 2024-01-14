-- Bảng Restaurant
CREATE TABLE Restaurant (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(255),
    email VARCHAR(255),
    
);

-- Bảng Customers
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(255),
    email VARCHAR(255),
    restaurant_id INT,

    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
);

-- Bảng Employees
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(255),
    position VARCHAR(255),
    salary DECIMAL(10,2),
    date_of_birth DATE,
    restaurant_id INT,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
);

-- Bảng Orders
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    employee_id INT,
    date DATE,
    total DECIMAL(10,2),
    payment_status VARCHAR(20),

    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Bảng Dishes
CREATE TABLE Dishes (
    dish_id INT PRIMARY KEY,
    dish_name VARCHAR(255),
    description VARCHAR(255),
    price DECIMAL(10,2),
    preparation_time INT,
);

-- Bảng Ingredients
CREATE TABLE Ingredients (
    ingredient_id INT PRIMARY KEY,
    ingredient_name VARCHAR(255),
    unit VARCHAR(50),
    supplier VARCHAR(255),
    
);

-- Bảng Categories
CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(255),
    
);

-- Bảng Suppliers
CREATE TABLE Suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(255),
);



-- Bảng DishIngredients, biểu diễn mối quan hệ n-n giữa Dishes và Ingredients
CREATE TABLE DishIngredients (
    dish_id INT,
    ingredient_id INT,
    PRIMARY KEY (dish_id, ingredient_id),
    FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

-- Bảng DishCategories, biểu diễn mối quan hệ n-n giữa Dishes và Categories
CREATE TABLE DishCategories (
    dish_id INT,
    category_id INT,
    PRIMARY KEY (dish_id, category_id),
    FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Bảng DishSuppliers, biểu diễn mối quan hệ 1-1 giữa Dishes và Suppliers
CREATE TABLE DishSuppliers (
    dish_id INT,
    supplier_id INT,
    PRIMARY KEY (dish_id, supplier_id),
    FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);


CREATE TABLE DishOrders (
    dish_id INT,
    order_id INT,
    PRIMARY KEY (dish_id, order_id),
    FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);