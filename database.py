import mysql.connector
from config import DB_CONFIG
import logging

def initialize_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cr=conn.cursor()

    #cr.execute('create database if not exists ecommercebotdb')



    cr.execute('''
        CREATE TABLE IF NOT EXISTS user (
            cid BIGINT UNSIGNED NOT NULL PRIMARY KEY,
            full_name VARCHAR(100),
            username VARCHAR(100),
            email VARCHAR(100),
            mobile_number VARCHAR(15),
            registered_date DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')    

    cr.execute('''
        CREATE TABLE IF NOT EXISTS product (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            category ENUM('shirts', 'pants','shoes','hats','jackets') NOT NULL,
            name VARCHAR(50) NOT NULL,
            price double(10,2) NOT NULL,
            inventory SMALLINT UNSIGNED DEFAULT 1,
            description TEXT,
            img VARCHAR(150),
            added_date DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')    





    cr.execute('''
        CREATE TABLE IF NOT EXISTS `order` (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            cid BIGINT UNSIGNED,
            date_ordered DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cid) REFERENCES user(cid) ON DELETE SET NULL
        );
    ''')

    cr.execute('''
        CREATE TABLE IF NOT EXISTS orderItem (
            orderItem_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            order_id INT,
            quantity SMALLINT UNSIGNED DEFAULT 1,
            FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE SET NULL,
            FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE CASCADE
        );
    ''')

    cr.execute('''
        CREATE TABLE IF NOT EXISTS shipping (
            shipping_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            `address` TEXT,
            FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE SET NULL
        );
    ''')
    
    conn.commit()
    conn.close()

initialize_db()