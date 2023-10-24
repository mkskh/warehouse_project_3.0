from data import stock
from datetime import datetime
import get_and_greet_user
import sys


user_name = get_and_greet_user.get_user_name()
get_and_greet_user.greet_user(user_name)

def get_selected_operation():
    '''Ask user what he/she want to choose from menu'''
    print('\nWhat would you like to do?: \n1. Show list items by warehouse\n2. Search an item and place an order\n3. Browse by category \n4. Quit')
    choice = input('Type the number of the operation: ')
    return choice


def list_items_by_warehouse():
    '''List the items by warehouse'''
    total_items = {}
    print('\nItems in warehouses:\n')
    for position in stock:
        if position['warehouse'] not in total_items:
            total_items[position['warehouse']] = 1
        elif position['warehouse'] in total_items:
            total_items[position['warehouse']] += 1
        print(position['state'], position['category'])
    print('')
    for number in range(1, len(total_items) + 1):
        print(f'Total items in warehouse {number}: ', total_items[number])
    termination(user_name)


def search_and_order_item():
    '''Search and order item'''
    desired_product = input(f'\nWhat is the name of the item? ')
    product_quantity_by_locations = {}                    
    bigger_quantity = 0
    bigger_warehouse = 0
    time_now = datetime.now().date()
    location = []

    # Count products, define warehouse and count days
    for position in stock:
        name = [position['state'], position['category']]
        name = ' '.join(name)
        if name.lower() == desired_product.lower():
            time_stored = position['date_of_stock']
            time_stored = datetime.strptime(time_stored, "%Y-%m-%d %H:%M:%S").date()
            delta = time_now - time_stored
            if position['warehouse'] not in product_quantity_by_locations:  # count quantity of items by warehouses
                product_quantity_by_locations[position['warehouse']] = 1
            elif position['warehouse'] in product_quantity_by_locations:
                product_quantity_by_locations[position['warehouse']] += 1
            warehouse = position['warehouse']
            location.append(f'- Warehouse {warehouse} (in stock for {delta.days} days)')
            
    '''Count total products in two warehouses'''
    total_quantity = len(location)
    if total_quantity == 0:
        print('Item not found')
        termination(user_name)
    location.sort()

    if total_quantity == 0:
        '''Item not found'''
        print(f'Amount available: {total_quantity}\nLocation: Not in stock')
    else:
        print(f'Amount available: {total_quantity}\nLocation:')

    sorted_product_quantity_by_locations = sorted(product_quantity_by_locations.items(), key=lambda x:x[1], reverse=True)
    new_sorted_product_quantity_by_locations = dict(sorted_product_quantity_by_locations)
    bigger_quantity = list(new_sorted_product_quantity_by_locations.values())[0]
    bigger_warehouse = list(new_sorted_product_quantity_by_locations.keys())[0]

    '''List every item'''
    for item in location:
        print(item)
    print(f'\nMaximum availability: {bigger_quantity} in Warehouse {bigger_warehouse}\n')

    # ak user does he/she want to order an item
    order_decision = input('Would you like to order this item?(y/n) ') 
    if order_decision == 'n':
        '''Disagree'''
        None
    elif order_decision == 'y':
        '''Agree'''
        order_quantity = int(input('How many would you like? '))
        if order_quantity > total_quantity:
            message_for_customer(total_quantity)
            '''Order more than available (accepting and not accepting)'''
            repeat_order_decision = input('Would you like to order the maximum available?(y/n) ')
            if repeat_order_decision == 'n':
                None
            elif repeat_order_decision == 'y':
                print(f'{total_quantity} {desired_product} have been ordered.')
            else:
                print(f'Wrong choice. Please try again!')
        elif order_quantity <= total_quantity:
            '''Order the available quantity'''
            print(f'{order_quantity} {desired_product} have been ordered.')
        elif order_quantity <= 0:
            '''Order less than Zero'''
            print(f'Wrong quantity. Please try again!')
    else:
        '''Wrong choice'''
        print(f'Wrong choice. Please try again!')
    termination(user_name)

def browse_by_category():
    '''Browse items by category'''
    list_category = []
    dict_category = {}
    for position in stock:
        if position['category'] not in list_category:
            list_category.append(position['category'])
    print('')
    for i in range(1, len(list_category)+1):
        count = 0
        for position in stock:
            if position['category'] == list_category[i-1]:
                count += 1
        print(f'{i}. {list_category[i-1]} ({count})')
        dict_category[i] = list_category[i-1]

    choice_browse = int(input('Type the number of the category to browse: '))
    print('\nList of laptops available: ')
    for key, value in dict_category.items():
        if key == choice_browse:
            for position in stock:
                if value == position['category']:
                    print(position['state'], position['category'] +',', 'Warehouse', position['warehouse'])
    termination(user_name)


def thanks(user_name):
    print(f'\nThank you for your visit, {user_name}!')


def termination(user_name):   
    termination_choice = input('\nWould you like to perform another operation? (y/n) ')
    if termination_choice == 'n':
        thanks(user_name)
        sys.exit()
    elif termination_choice == 'y':
        main()
    else:
        valid_operation_message()



def decoration(func):
    '''Decorate the message by stars'''
    def inner(*args, **kwargs):
        print('*'*80)
        func(*args, **kwargs)
        print('*'*80)
    return inner


@decoration
def message_for_customer(quantity):
    print(f'There are not this many available. The maximum amount that can be ordered is {quantity}')


@decoration
def valid_operation_message():
    print('Search is not a valid operation.')


def main():


    operation = get_selected_operation()


    if operation == '1':
        list_items_by_warehouse()


    elif operation == '2':
        search_and_order_item()


    elif operation == '3':
        browse_by_category()


    elif operation == '4':
        pass


    else:
        print('')
        valid_operation_message()


thanks(user_name)


if __name__ == '__main__':
    main()
    thanks(user_name)




