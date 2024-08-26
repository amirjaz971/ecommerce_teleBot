import mysql.connector
from config import DB_CONFIG


def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        pass


def get_all_products(category=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if category:
            cursor.execute('SELECT product_id,name,price FROM product where category=%s',(category,))
        else:
            cursor.execute('SELECT product_id,name,price FROM product')
        products = cursor.fetchall()
        
        conn.close()
        return products
    except Exception as e:
        pass


def get_product_detail(product_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select * from product where product_id=%s',(product_id,))
        product=cursor.fetchone()
        cursor.execute('select file_id from product_images where product_id=%s',(product_id,))
        product_img=cursor.fetchall()
        conn.close()
        return product,product_img
    except Exception as e:
        pass


def add_product(data_lst):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute('insert into product(category, name, price, inventory, description) values(%s,%s,%s,%s,%s)',(data_lst[0],data_lst[1],data_lst[2],data_lst[3],data_lst[4]))
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        return 0



def remove_product(product_id):
    try:
        conn=get_db_connection()

        cursor=conn.cursor()

        cursor.execute('delete from product where product_id=%s',(product_id,))
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        return 0



def add_to_cart(cid,product_id,quantity):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)

        
        cursor.execute('select order_id from `order` where cid=%s AND date_ordered is NULL',(cid,))
        order=cursor.fetchone()
        if order:
            order_id=order['order_id']
        else:
            cursor.execute('INSERT INTO `order`(cid,date_ordered) values(%s,NULL)',(cid,))
            order_id=cursor.lastrowid

        cursor.execute('SELECT inventory FROM PRODUCT WHERE product_id=%s',(product_id,))
        product=cursor.fetchone()
        if int(quantity)<=product['inventory']:
            cursor.execute('insert into orderItem(product_id,order_id,quantity) values(%s,%s,%s)',(product_id,order_id,quantity))


        
            
            



    except Exception as e:
        return 0





















def add_to_cart(chat_id, product_code, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO shopping_cart (chat_id, product_code, quantity) 
        VALUES (%s, %s, %s) 
        ON DUPLICATE KEY UPDATE quantity = quantity + %s
    ''', (chat_id, product_code, quantity, quantity))
    conn.commit()
    conn.close()

def get_cart_from_db(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.name, p.price, sc.quantity 
        FROM shopping_cart sc 
        JOIN products p ON sc.product_code = p.code 
        WHERE sc.chat_id = %s
    ''', (chat_id,))
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items

def remove_from_cart(user_id, product_code):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM cart 
        WHERE user_id = %s AND product_id = %s
    ''', (user_id, product_code))
    
    conn.commit()
    conn.close()
