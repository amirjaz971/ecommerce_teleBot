import mysql.connector
from config import DB_CONFIG
import logging
import datetime

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logging.exception(f"Error:{e}")


def get_product_price(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()    

        cursor.execute('select price from product where product_id=%s',(product_id,))   
        price=cursor.fetchone()

        if price:
            return price[0]
        else:
            return 0 
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()    


def fetch_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()    

        cursor.execute('SELECT DISTINCT category FROM product')   
        categories=cursor.fetchall()
        if categories:
            return categories
        else:
            return 0 
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def get_or_create_user(cid):

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('select cid from user where cid=%s',(cid,))
        user=cursor.fetchone()
        if not user:
            cursor.execute('insert into user(cid) values(%s)',(cid,))
            conn.commit()

        return 1



    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()



def get_all_products(category=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if category:
            cursor.execute('SELECT product_id,name,price FROM product where category=%s',(category,))
        else:
            cursor.execute('SELECT product_id,name,price FROM product')
        products = cursor.fetchall()
        

        return products
    except Exception as e:
        logging.error(f"Error:{e}")
    finally:
        cursor.close()
        conn.close()

def get_product_detail(product_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select * from product where product_id=%s',(product_id,))
        product=cursor.fetchone()
        
        if product:
            return product
        else:
            return 0
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()

def add_product(data_lst):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute('insert into product(category, name, price, inventory, description,img) values(%s,%s,%s,%s,%s,%s)',(data_lst[0].lower(),data_lst[1],data_lst[2],data_lst[3],data_lst[4],data_lst[5]))
        conn.commit()

        return 1
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def remove_product(product_id):
    try:
        conn=get_db_connection()

        cursor=conn.cursor()

        cursor.execute('delete from product where product_id=%s',(product_id,))
        conn.commit()

        return 1
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def add_to_cart(cid,product_id,quantity=1):
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
        if product and int(quantity)<=product['inventory']:
            cursor.execute('SELECT * FROM orderItem WHERE product_id=%s AND order_id=%s', (product_id, order_id))
            order_item = cursor.fetchone()
            if order_item:
                cursor.execute('UPDATE orderItem SET quantity=%s WHERE product_id=%s AND order_id=%s', 
                               (quantity, product_id, order_id))
            else:
                cursor.execute('INSERT INTO orderItem(product_id, order_id, quantity) VALUES (%s, %s, %s)', 
                               (product_id, order_id, quantity))
        else:
            return False
        conn.commit()
        return True
    except Exception as e:
        logging.exception(f"Error:{e}")
        return False
    finally:
        cursor.close()
        conn.close()


def checkout(cid,address):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select order_id from `order` where cid=%s AND date_ordered is NULL',(cid,))
        order=cursor.fetchone()
        if order:
            order_id=order['order_id']
        else:
            return False
        now=datetime.datetime.now()
        cursor.execute('UPDATE `order` set date_ordered=%s where order_id=%s',(now,order_id))
        cursor.execute('insert into shipping (order_id,address) values(%s,%s)',(order_id,address))
        cursor.execute('select * from shipping where order_id=%s',(order_id,))
        shipping=cursor.fetchone()
        conn.commit()
        if shipping:
            return shipping
        else:
            return False

    except Exception as e:
        logging.exception(f"Error:{e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_profile_data(cid):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select * from user where cid=%s',(cid,))
        user=cursor.fetchone()

        if user:
            return user
        else:
            return 0


    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()

def profile_settings(cid,full_name=None,username=None, email=None, mobile_number=None,):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('update user set full_name=%s,username=%s,email=%s,mobile_number=%s where cid=%s ',(full_name,username,email,mobile_number,cid))


        conn.commit()
        return 1
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0

    finally:
        cursor.close()
        conn.close()

def get_all_orders(cid):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select * from `order` where cid=%s',(cid,))
        orders=cursor.fetchall()
        if orders:
            return orders
        else:
            return 0


    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def get_order_detail(cid,order_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select * from `order` inner join orderItem on order.order_id=orderItem.order_id where order.cid=%s AND order.order_id=%s',(cid,order_id))
        order_detail=cursor.fetchall()
        if order_detail:
            return order_detail
        else:
            return 0


    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def get_all_users():
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select cid,registered_date from user')
        users=cursor.fetchall()
        if users:
            return users
        else:
            return 0
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0

    finally:
        cursor.close()
        conn.close()


def get_user_detail(user_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select * from user where cid=%s',(user_id,))
        user=cursor.fetchone()
        if user:
            return user
        else:
            return 0

    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0

    finally:
        cursor.close()
        conn.close()


def uncompleted_order(cid):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select order_id from `order` where cid=%s AND date_ordered is NULL',(cid,))
        order=cursor.fetchone()
        if order:
            order_id=order['order_id']
        else:
            return False
        cursor.execute('select * from orderItem where order_id=%s',(order_id,))
        order_items=cursor.fetchall()

        if order_items:
            return order_items
        return False
        
    except Exception as e:
        logging.exception(f"Error:{e}")
        return False
    
    finally:
        cursor.close()
        conn.close()



def get_all_shippings(cid):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select * from shipping where cid=%s',(cid,))
        shippings=cursor.fetchall()

        if shippings:
            return shippings
        else:
            return False


    except Exception as e:
        logging.exception(f"Error:{e}")
        return False
    finally:
        cursor.close()
        conn.close()  



def remove_from_cart(cid,orderItem_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('select order_id from `order` where cid=%s AND date_ordered is NULL',(cid,))
        order=cursor.fetchone()
        if order:
            order_id=order['order_id']
        else:
            return 0        
        cursor.execute('delete from orderItem where orderItem_id=%s AND order_id=%s',(orderItem_id,order_id))
        
        conn.commit()
        return 1
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()



def cancel_order(cid):
    try:
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute('delete from `order` where cid=%s AND date_ordered is NULL',(cid,))
        conn.commit()
        return 1
    except Exception as e:
        logging.exception(f"Error:{e}")
        return 0
    finally:
        cursor.close()
        conn.close()
