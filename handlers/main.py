
from config import Channel_cid, admins,bot,logging
from utils.database_utils import  get_all_products,get_product_detail,add_product,remove_product,add_to_cart, get_cart_from_db,remove_from_cart
from messages import command_default
from handlers import messages, callback_queries, photos
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup,KeyboardButton



if __name__=='__main__':
    user_step=dict()
    hideboard = ReplyKeyboardRemove()

    commands={
        'start':'Welcome message and basic instructions',
        'help':'Display help message',
        'list_products':'List products by category',
        'product_detail':'Product detail by ID',
        'view_cart':'View your shopping cart',
        'add_to_cart':'Add a product to your cart',
        'remove_from_cart':'Remove a product from your cart',
        'profile':'View or update your profile information',
        }

    admin_commands={
        'add_product':'Add product to the list',
        'remove_product':'Remove product from the list',
        'update_product':'Update product',
    }


    @bot.message_handler(commands=['start'])
    def start_command(message):
        cid = message.chat.id
        bot.send_message(cid, 'Welcome to the ECommerce bot! Use /help to see available commands.')



    @bot.message_handler(commands=['help'])
    def help_command(message):
        cid = message.chat.id
        text = 'Available commands:\n'
        for key in commands:
            text+=f"/{key} - {commands[key]}\n"
        if cid in admins:
            for key_admin in admin_commands:
                text+=f"/{key_admin} - {admin_commands[key_admin]}\n"

        bot.send_message(cid, text)




    @bot.message_handler(commands=['list_products'])
    def list_products_command(message):
        cid = message.chat.id
        bot.send_message(cid,'Enter the category')
        user_step[cid]=0


    
 

    @bot.message_handler(commands=['product_detail'])
    def product_detail_command(message):
        cid=message.chat.id
        bot.send_message(cid,'Enter the product ID')
        user_step[cid]=1


    @bot.message_handler(commands=['add_product'])
    def add_product_command(message):
        cid=message.chat.id
        if cid in admins:

            bot.send_message(cid,'To add product use this format: category,name,price,inventory,description')
            user_step[cid]=2
        else:
            command_default(message)



    @bot.message_handler(commands=['remove_product'])
    def remove_product_command(message):
        cid=message.chat.id
        if cid in admins:
            bot.send_message(cid,'Enter the ID to remove the product')
            user_step[cid]=3
        else:
            command_default(message)   




    @bot.message_handler(commands=['add_to_cart'])
    def add_to_cart_command(message):
        cid = message.chat.id
        parts = message.text.split()
        if len(parts) != 3:
            bot.send_message(cid, 'Usage: /add_to_cart <product_code> <quantity>')
            return
        
        product_code = int(parts[1])
        quantity = int(parts[2])
        
        add_to_cart(cid, product_code, quantity)
        bot.send_message(cid, f'Added {quantity} of product code {product_code} to your cart.')








    @bot.message_handler(commands=['view_cart'])
    def view_cart_command(message):
        cid = message.chat.id
        cart_items = get_cart_from_db(cid)
        if cart_items:
            response = 'Your cart:\n'
            for index, item in enumerate(cart_items, start=1):
                response += f"{index}. Name: {item[0]}, Price: ${item[1]}, Quantity: {item[2]}\n"
            response += '\nUse /remove_from_cart <item_name> to remove an item by its name.'
            bot.send_message(cid, response)
        else:
            bot.send_message(cid, 'Your cart is empty.')

    @bot.message_handler(commands=['remove_product'])
    def remove_from_cart_command(message):
        cid = message.chat.id
        parts = message.text.split(maxsplit=1)
        
        if len(parts) != 2:
            bot.send_message(cid, 'Usage: /remove_from_cart <item_name>')
            return

        item_name = parts[1].strip()
        
        # Get cart items to find the product code associated with the item name
        cart_items = get_cart_from_db(cid)
        product_code = None
        
        for item in cart_items:
            if item[0].lower() == item_name.lower():
                product_code = item[3]  # Assuming product_code is the 4th element
                break

        if not product_code:
            bot.send_message(cid, 'Item not found in your cart.')
            return

        # Remove the item from the cart
        remove_from_cart(cid, product_code)
        bot.send_message(cid, f'Removed "{item_name}" from your cart.')










    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==0)
    def get_product_category_to_display(message):
        cid=message.chat.id
        category=message.text.strip()
        products=get_all_products(category)
        if products:
            response='Available products:\n\n'
            for product in products:
                response+=f"ID: {product['product_id']}\nName: {product['name']}\nPrice: ${product['price']}\nInventory: {product['inventory']}\n\n"
            bot.send_message(cid,response)    
        else:
            bot.send_message(cid, 'No products available.')

        user_step[cid]=-1    



    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==1)
    def get_product_id_to_display(message):
        cid=message.chat.id
        product_id=message.text.strip()
        try:
            
            product,img=get_product_detail(product_id)
            if product:
                response='Product detail\n\n'
                for key in product:

                    response+=f"{key}: {product[key]}\n\n"
                bot.send_message(cid,response)
            else:
                bot.send_message(cid,'Product not found!')
        except ValueError:
            bot.send_message(cid,'ID must be integer!')    

        user_step[cid]=-1 


            

    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==2)
    def get_product_datas_to_add(message):
        cid=message.chat.id
        datas=message.text
        try:
            datas_lst=datas.split(',')
            response=add_product(datas_lst)
            if response==1:
                bot.send_message(cid,'Datas have been added successfully')
            else:
                bot.send_message(cid,'Adding datas failed due to these possible reasons:\n1-Product not found\n2-Datas are wrong')
        except:
            bot.send_message(cid,'Please enter the datas with the given format')
        user_step[cid]=-1    


    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==3)
    def get_product_id_to_remove(message):
        cid=message.chat.id
        product_id=message.text.strip()
        response=remove_product(product_id)

        if response==1:
            bot.send_message(cid,'Product has been deleted successfully')
        else:
            bot.send_message(cid,'Removing product failed due to these possible reasons:\n1-Product not found\n2-product ID is wrong')
        user_step[cid]=-1






# @bot.callback_query_handler(func=lambda call: True)
# def callback_query_function(call):
#     # print(call.message.reply_markup.keyboard[0][1].text)
#     call_id = call.id
#     cid = call.message.chat.id
#     mid = call.message.message_id
#     data = call.data
#     print(f'button pressed, id: {call_id}, cid: {cid}, message id: {mid}, data: {data}')
#     if data.startswith('change'):
#         command, code, new_qty = data.split('_')
#         if new_qty == '0':
#             bot.answer_callback_query(call_id, f'quantity cannot be zero')
#         else:
#             caption, new_markup = generate_product_markup(int(code), int(new_qty))
#             bot.edit_message_caption(caption, cid, mid)
#             bot.edit_message_reply_markup(cid, mid, reply_markup=new_markup)
#             bot.answer_callback_query(call_id, f'quantity changed to {new_qty}')
#     elif data == 'cancel':
#         bot.answer_callback_query(call_id, f'operation canceled')
#         bot.edit_message_reply_markup(cid, mid, reply_markup=None)
#         bot.delete_message(cid, mid)        
#     elif data.startswith('add'):
#         command, code, qty = data.split('_')
#         shopping_cart.setdefault(cid, dict())
#         shopping_cart[cid][int(code)] = int(qty)
#         bot.answer_callback_query(call_id, f'{qty} itme {code} added to basket')
#         markup = InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton('✅ added to basket', callback_data='show_basket'))
#         bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
#     elif data == 'show_basket':
#         basket = shopping_cart[cid]
#         bot.send_message(cid, f'your shopping cart: {basket}')


        


    bot.message_handler(func=lambda m: True, content_types=['photo'])(photos.photo_message_handle)


    bot.message_handler(func=lambda m: True, content_types=['text'])(messages.command_default)


    bot.infinity_polling(skip_pending=True)