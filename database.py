import mysql.connector


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password', #Please enter your password
    'port': 3306,
    
}

def initialize_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cr=conn.cursor()

    cr.execute('create database if not exists ecommercebotdb')
    cr.execute('USE ecommercebotdb')


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

    cr.execute('SELECT COUNT(*) FROM product')
    product_count = cr.fetchone()[0]
    if product_count==0:
        products = [
            ('shirts', 'Classic White Shirt', 29.99, 10, 'A stylish classic white shirt, perfect for formal and casual wear.', 'product_images/shirts/classic_white_shirt.jpg'),
            ('pants', 'Denim Jeans', 49.99, 15, 'Comfortable and durable denim jeans in various sizes.', 'product_images/pants/denim_jeans.jpg'),
            ('shoes', 'Running Shoes', 79.99, 25, 'Lightweight and comfortable running shoes for daily use.', 'product_images/shoes/running_shoes.jpg'),
            ('hats', 'Baseball Cap', 19.99, 50, 'Adjustable baseball cap with a curved brim.', 'product_images/hats/baseball_cap.jpg'),
            ('jackets', 'Leather Jacket', 99.99, 5, 'Premium leather jacket for a sleek and modern look.', 'product_images/jackets/leather_jacket.jpg')
        ]


        query = '''
            INSERT INTO product (category, name, price, inventory, description, img) 
            VALUES (%s, %s, %s, %s, %s, %s);
        '''


        for product in products:
            cr.execute(query, product)



        print("Products inserted successfully!")

    else:
        print('products has been inserted already')
    print('Connected to the database')
    conn.commit()
    conn.close()

initialize_db()













