
from config import admins,bot,logging
from utils.database_utils import  fetch_categories,get_or_create_user,get_all_products,get_product_detail,add_product,remove_product,add_to_cart, view_cart,remove_from_cart,checkout,get_profile_data,profile_settings,get_all_orders,get_order_detail,get_all_users,get_user_detail
from messages import command_default
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
        'checkout':'Finalize the order and shipping',
        'profile_view':'View your profile information',
        'profile_settings':'Edit your profile information',
        'order_history':'View all completed orders',
        'order_detail':'View completed order detail',
        }

    admin_commands={
        'add_product':'Add product to the list',
        'remove_product':'Remove product from the list',
        'update_product':'Update product',
        'view_users':'View all users',
        'view_user_detail':'View user detail',    
    }


    @bot.message_handler(commands=['start'])
    def start_command(message):
        cid = message.chat.id
        response=get_or_create_user(cid)
        if response==1:
            bot.send_message(cid, 'Welcome to the ECommerce bot! Use /help to see available commands.')
        else:
            bot.send_message(cid,'Error occured please enter the /start command again')


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
        reply_keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
        categories=fetch_categories()
        if categories!=0:
            
            
            for category in categories:
                reply_keyboard.add(category[0])
            bot.send_message(cid,'choose the category',reply_markup=reply_keyboard)
            user_step[cid]=0
        else:
            bot.send_message(cid,'Nothing found!')
        
        


    
 

    @bot.message_handler(commands=['product_detail'])
    def product_detail_command(message):
        cid=message.chat.id
        bot.send_message(cid,'Enter the product ID')
        user_step[cid]=1


    @bot.message_handler(commands=['add_product'])
    def add_product_command(message):
        cid=message.chat.id
        if cid in admins:

            bot.send_message(cid,'To add product please send image and the caption using this format: category,name,price,inventory,description\n\nAvailable categories: shirts,pants,shoes,hats,jackets')
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


    @bot.message_handler(commands=['view_cart'])
    def view_cart_command(message):
        cid = message.chat.id


    @bot.message_handler(commands=['add_to_cart'])
    def add_to_cart_command(message):
        cid = message.chat.id

        bot.send_message(cid,"Enter the product ID and quantity with this format:product_id,quantity")
        user_step[cid]=4
        

    @bot.message_handler(commands=['remove_from_cart'])
    def remove_from_cart_command(message):
        cid = message.chat.id
        user_step[cid]=5





    @bot.message_handler(commands=['checkout'])
    def checkout_command(message):
        cid=message.chat.id
        bot.send_message(cid,'Enter the address to check and ship the order')
        user_step[cid]=6


    @bot.message_handler(commands=['profile_view'])
    def profile_view_command(message):
        cid=message.chat.id
        profile_data=get_profile_data(cid)
        if profile_data!=0:
            text='Profile Information:\n\n'
            for key in profile_data:
                text+=f"{key}: {profile_data[key]}\n\n"
            bot.send_message(cid,text)
        else:
            bot.send_message(cid,'Nothing found!')



    @bot.message_handler(commands=['profile_settings'])
    def profile_settings_command(message):
        cid=message.chat.id
        bot.send_message(cid,'Enter the datas with this format to edit your profile:full_name,username,email,mobile_number')
        user_step[cid]=7



    @bot.message_handler(commands=['order_history'])
    def order_history_command(message):
        cid=message.chat.id
        orders=get_all_orders(cid)
        if orders!=0:
            text='All Orders:\n\n'
            for order in orders:
                for key in order:
                    text+=f"{key}: {order[key]}\n\n"
            bot.send_message(cid,text)
        else:
            bot.send_message(cid,'Nothing found!')


    @bot.message_handler(commands=['order_detail'])
    def order_detail_command(message):
        cid=message.chat.id
        bot.send_message(cid,'Enter the Order ID to display order details')
        user_step[cid]=8




    @bot.message_handler(commands=['view_users'])
    def view_users_command(message):
        cid=message.chat.id
        if cid in admins:
            users=get_all_users()
            if users!=0:
                text='Users:\n\n'
                for user in users:
                    for key in user:
                        text+=f"{key}: {user[key]}\n\n"
                bot.send_message(cid,text)
            else:
                bot.send_message(cid,'Nothing found!')
        else:
            command_default(message)
                

    @bot.message_handler(commands=['view_user_detail'])
    def view_user_detail_command(message):
        cid=message.chat.id
        if cid in admins:
            bot.send_message(cid,'Enter the user ID to display user detail')
            user_step[cid]=9

        else:
            command_default(message)










    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==0)
    def get_product_category_to_display_func(message):
        cid=message.chat.id
        category=message.text.strip()
        products=get_all_products(category)
        if products:
            response='Available products:\n\n'
            for product in products:
                response+=f"ID: {product['product_id']}\nName: {product['name']}\nPrice: ${product['price']}\n\n"
            bot.send_message(cid,response)    
        else:
            bot.send_message(cid, 'No products available.')

        user_step[cid]=-1    



    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==1)
    def get_product_id_to_display_func(message):
        cid=message.chat.id
        
        try:
            product_id=message.text.strip()
            product=get_product_detail(product_id)
            if product!=0:
                product_info = (
                    
                    f"**ID:** {product['product_id']}\n"
                    f"**Category:** {product['category']}\n"
                    f"**Product Name:** {product['name']}\n"
                    f"**Price:** ${product['price']}\n"
                    f"**Description:** {product['description']}\n"
                    f"**Added Date:** {product['added_date']}"
                )
                    
                if product['img']:
                    with open(product['img'],'rb') as photo:
                        bot.send_photo(cid,photo,caption=product_info,parse_mode='Markdown')
                else:
                    bot.send_message(cid,product_info,parse_mode='Markdown')
            else:
                bot.send_message(cid,'Product not found!')
        except Exception as e:
            bot.send_message(cid, 'Please provide a valid product ID.')    

        user_step[cid]=-1 




    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==3)
    def get_product_id_to_remove_func(message):
        cid=message.chat.id
        product_id=message.text.strip()
        response=remove_product(product_id)

        if response==1:
            bot.send_message(cid,'Product has been deleted successfully')
        else:
            bot.send_message(cid,'Removing product failed due to these possible reasons:\n1-Product not found\n2-product ID is wrong')
        user_step[cid]=-1



    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==4)
    def add_to_cart_func(message):
        pass






    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==5)
    def remove_from_cart_func(message):
        pass




    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==6)
    def checkout_func(message):
        pass


    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==7)
    def profile_settings_func(message):
        pass


    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==8)
    def order_detail_func(message):
        cid=message.chat.id
        order_id=message.text.strip()
        order_detail=get_order_detail(cid,order_id)
        if order_detail!=0:
            text='Order Detail:\n\n'
            for order in order_detail:
                for key in order:
                    text+=f"{key}: {order[key]}\n\n"
            bot.send_message(cid,text)

        else:
            bot.send_message(cid,'Nothing found!')        

        user_step[cid]=-1

    @bot.message_handler(func=lambda m:user_step.get(m.chat.id,'Error occurred during responsing')==9)
    def view_user_detail_func(message):
        cid=message.chat.id
        user_id=message.text.strip()
        user=get_user_detail(user_id)
        if user!=0:
            text='User Detail:\n\n'
            for key in user:
                text+=f"{key}: {user[key]}\n\n"
            bot.send_message(cid,text)

        else:
            bot.send_message(cid,'Nothing found!')
        user_step[cid]=-1




    @bot.message_handler(content_types=['photo'])
    def handle_product_image(message):
        cid=message.chat.id
        if user_step.get(cid)==2:
            if message.caption:
                data_lst=message.caption.split(',')
                if len(data_lst)==5:
                    try:
                        file_info=bot.get_file(message.photo[-1].file_id)
                        
                        downloaded_file=bot.download_file(file_info.file_path)
                        img_path=f'product_images/{file_info.file_path.split("/")[-1]}'
                        with open(img_path,'wb') as new_file:
                            new_file.write(downloaded_file)

                        data_lst.append(img_path)
                        response=add_product(data_lst)
                        if response==1:
                            bot.send_message(cid,'Product has been added successfully')
                        else:
                            bot.send_message(cid,'Failed to add product')
                    except Exception as e:
                        bot.send_message(cid,f"Error: {e}")
                else:
                    bot.send_message(cid,'Incorrect format. Please use: category,name,price,inventory,description')
            else:
                bot.send_message(cid,'Please provide caption for product details')
        else:
            bot.send_message(cid,'Please use /add_product command')    






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


        


    


    bot.message_handler(func=lambda m: True, content_types=['text'])(command_default)


    bot.infinity_polling(skip_pending=True)