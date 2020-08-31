class Item:

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
        

class VendingMachine:
    
    def __init__(self, slots=9):
        self.available_slots = slots
        self.total_slots = slots
        self.slot_items = {i: None for i in range(1, slots+1)}

        self.current_balance = 0

    def add_item_to_slot(self, target_slot, item, replace=False):
        """Add to the specified slot in the vending machine.

        Args:
            target_slot (int)
            item (Item)
            replace (bool)

        Returns:
            bool: flag indicating whether or not the item was added.

        """
        added = False

        if not self._is_valid_slot(target_slot):
            return added

        current_slot_item = self.slot_items[target_slot]

        if current_slot_item is not None:
            if current_slot_item.name == item.name:
                self.slot_items[target_slot].price = item.price
                self.slot_items[target_slot].stock += item.stock
                added = True
            elif replace:
                self.slot_items[target_slot] = item
                added = True
        else:
            self.slot_items[target_slot] = item
            self.available_slots -= 1
            added = True

        return added

    def move_item_to_slot(self, source_slot, target_slot, replace=False):
        """Move item from one slot to another.

        Args:
            source_slot (int)
            target_slot (int)
            replace (bool): whether or not to replace the item in the target slot.

        Returns:
            bool: flag indicating whether or not the item was moved.

        """
        moved = False

        if self._is_valid_slot(source_slot) and self._is_valid_slot(target_slot) \
                and self.slot_items[source_slot] is not None:

            if self.slot_items[target_slot] is None or replace:
                item = self.slot_items[source_slot]
                self.slot_items[source_slot] = None
                self.slot_items[target_slot] = item
                moved = True

        return moved

    def remove_item_from_slot(self, target_slot):
        """Remove from the specified slot in the vending machine.

        Args:
            target_slot (int)

        Returns:
            bool: flag indicating whether or not the item was removed.

        """
        removed = False

        if not self._is_valid_slot(target_slot) or self.available_slots == self.total_slots:
            return removed

        current_slot_item = self.slot_items[target_slot]

        if current_slot_item is not None:
            self.slot_items[target_slot] = None
            self.available_slots += 1
            removed = True

        return removed

    def replace_item_in_slot(self, target_slot, item):
        """Replace the item in the target slot with the specified item.

        Args:
            target_slot (int)
            item (Item)

        Returns:
            bool: flag indicating whether or not the item was replaced.

        """
        replaced = False

        if self._is_valid_slot(target_slot):
            if self.slot_items[target_slot] is None:
                self.available_slots -= 1

            self.slot_items[target_slot] = item
            replaced = True

        return replaced

    def change_name(self, target_slot, new_name):
        """Change the name of the item in the target slot.

        Args:
            target_slot (int)
            new_name (str)

        Returns:
            bool: flag indicating whether or not the name of the item was changed.

        """
        changed = False

        if self._is_valid_slot(target_slot) and self.slot_items[target_slot] is not None:
            self.slot_items[target_slot].name = new_name
            changed = True

        return changed
    
    def change_price(self, target_slot, new_price):
        """Change the price of the item in the target slot.

        Args:
            target_slot (int)
            new_price (int/float)

        Returns:
            bool: flag indicating whether or not the price of the item was changed.

        """
        changed = False

        if self._is_valid_slot(target_slot) and self.slot_items[target_slot] is not None:
            self.slot_items[target_slot].price = new_price
            changed = True

        return changed
    
    def increase_stock(self, target_slot, n=1):
        """Increase the stock of an item in the target slot.

        Args:
            target_slot (int)
            n (int)

        Returns:
            bool: flag indicating whether or not the stock was increased.
            int: the newly increased stock of the item.

        """
        increased = False
        new_stock = 0

        if self._is_valid_slot(target_slot) and self.slot_items[target_slot] is not None:
            current_stock = self.slot_items[target_slot].stock
            new_stock = current_stock + n
            self.slot_items[target_slot].stock = new_stock
            increased = True

        return increased, new_stock

    def decrease_stock(self, target_slot, n=1):
        """Decrease the stock of an item in the target slot.

        Args:
            target_slot (int)
            n (int)

        Returns:
            bool: flag indicating whether or not the stock was decreased.
            int: the newly decreased stock of the item.
            
        """
        decreased = False
        new_stock = 0

        if self._is_valid_slot(target_slot) and self.slot_items[target_slot] is not None:
            current_stock = self.slot_items[target_slot].stock

            if n > current_stock:
                new_stock = 0
            else:
                new_stock = current_stock - n

            self.slot_items[target_slot].stock = new_stock

            decreased = True

        return decreased, new_stock
    
    def insert_money(self, amount):
        """Insert money into the vending machine.

        Args:
            amount (int/float)

        Returns:
            bool: flag indicating whether or not the amount was inserted.
            float: the current total balance after the transaction.

        """
        if amount > 0:
            self.current_balance += amount
            return True, self.current_balance
        else:
            return False, self.current_balance

    def remove_money(self, amount):
        """Remove money from the vending machine.

        If the amount to remove is higher than the total balance, remove the entire total balance.

        Args:
            amount (int/float)

        Returns:
            bool: flag indicating whether or not the amount was removed.
            float: the current total balance after the transaction.

        """
        if amount > 0 and self.current_balance > 0:
            if amount > self.current_balance:
                self.current_balance = 0
            else:
                self.current_balance -= amount

            return True, self.current_balance
        else:
            return False, self.current_balance
        
    def select_and_vend(self, slot_number):
        """Vends the item at the slot number.

        If there is a sufficient total balance and the item is not out of stock, the item will vend.

        Args:
            slot_number (int)

        Returns:
            bool: flag indicating whether or not the item was vended.
            str: summary of the item vended.
            str: reason explaining the vend success or failure.
            float: the remaining total balance.

        """
        vended, item_summary, vend_result = False, '', ''

        if not self._is_valid_slot(slot_number):
            return vended, item_summary, 'Invalid Slot', self.current_balance

        current_slot_item = self.slot_items[slot_number]

        if current_slot_item is None:
            return vended, item_summary, 'Empty Slot', self.current_balance
        else:
            item_summary = self._get_abstract(current_slot_item.name)

            if self.current_balance < current_slot_item.price:
                return vended, item_summary, 'Insufficient Balance', self.current_balance
            elif current_slot_item.stock <= 0:
                return vended, item_summary, 'Out of Stock', self.current_balance
            else:
                self.current_balance -= current_slot_item.price
                current_slot_item.stock -= 1

                vend_result = f'Vended: {current_slot_item.name}'

                vended = True

        return vended, item_summary, vend_result, self.current_balance

    """PRIVATE METHODS"""

    def _is_valid_slot(self, slot):
        return 0 < slot <= self.total_slots

    def _get_abstract(self, search_term):
        import requests

        request_params = {
            'q': search_term.lower(),
            'format': 'json',
            'pretty': 1
        }

        search_url = 'https://api.duckduckgo.com'

        abstract = ''
        try:
            response = requests.get(url=search_url, params=request_params).json()
            abstract = response.get('AbstractText', '')
        except requests.exceptions.RequestException as e:
            print(f'Could not establish a connection to the DuckDuckGo API!\n{e}')

        return abstract


class VendingMachineInterface:

    def __init__(self):
        self.vending_machine = VendingMachine()
        self.maintenance_mode = False

        # Initial items
        self.vending_machine.add_item_to_slot(1, Item('Sparkling Water', 1.25, 20))
        self.vending_machine.add_item_to_slot(5, Item('Soda', 0.75, 20))
        self.vending_machine.add_item_to_slot(8, Item('Coffee', 1.75, 20))
        self.vending_machine.add_item_to_slot(9, Item('Energy Drink', 1.50, 20))

    def run(self):
        print('=' * 21)
        print('== ' + 'VENDING MACHINE' + ' ==')
        print('=' * 21)
        print()

        selected_option = self.customer_menu()

        while selected_option != 'q':
            if self.maintenance_mode:
                selected_option = self.maintenance_menu()
            else:
                selected_option = self.customer_menu()

    def customer_menu(self):

        selected_option = ''

        while selected_option != 'q':
            selectable_slots = set()

            print(f'Current balance: ${self.vending_machine.current_balance}\n')
            print('==== SLOT ITEMS ====')
            for slot_number, slot_item in self.vending_machine.slot_items.items():
                if slot_item:
                    print(f'[{slot_number}] {slot_item.name} - ${slot_item.price} (Remaining: {slot_item.stock})')
                    selectable_slots.add(slot_number)
            print()
            print('(i) Insert Money')
            print('(r) Remove Money')
            print('(m) Maintenance Mode')
            print('(q) Exit Vending Machine')

            selected_option = input('\nPlease select an option: ').lower()

            try:
                selected_option_int = int(selected_option)
            except ValueError:
                selected_option_int = -1

            if selected_option_int in selectable_slots:
                vended, item_summary, vend_result, total_balance = \
                    self.vending_machine.select_and_vend(selected_option_int)

                if vended:
                    print(vend_result)
                    if item_summary:
                        print(item_summary)
                    print(f'\nYour new balance is: ${total_balance}')
                else:
                    print(f'Unable to vend item in slot {selected_option_int} for the '
                          f'following reason: {vend_result}')

            elif selected_option == 'i':
                try:
                    insert_amount = float(input('Please enter the amount you would like to insert: '))
                    inserted, new_balance = self.vending_machine.insert_money(insert_amount)
                    if inserted:
                        print(f'${insert_amount} inserted. Your new balance is: ${new_balance}')
                    else:
                        print(f'Could not insert ${insert_amount}')

                except ValueError:
                    print('Invalid character entered! Returning to menu...')

            elif selected_option == 'r':
                try:
                    remove_amount = float(input('Please enter the amount you would like to remove: '))
                    removed, new_balance = self.vending_machine.remove_money(remove_amount)
                    if removed:
                        print(f'${remove_amount} removed. Your new balance is: ${new_balance}')
                    else:
                        print(f'Could not remove ${remove_amount}')
                except ValueError:
                    print('Invalid character entered! Returning to menu...')

            elif selected_option == 'm':
                selected_option = self.maintenance_menu()
                if selected_option == 'm':
                    print('Returning to customer menu...')
                    selected_option = ''

            else:
                if selected_option_int != -1:
                    if 0 < selected_option_int <= self.vending_machine.total_slots:
                        print('This slot is empty! Please try again.')
                    else:
                        print('Invalid slot selected! Please try again.')
                elif selected_option != 'q':
                    print('Invalid character entered! Please try again.')

        return selected_option

    def maintenance_menu(self):

        selected_option = ''

        while selected_option != 'q' and selected_option != 'm':
            print('*' * 22)
            print('** MAINTENANCE MODE **')
            print('*' * 22)
            print()

            print('(a) Add Item')
            print('(d) Display Items')
            print('(mod) Modify Existing Item')
            print('(mov) Move Item')
            print('(rem) Remove Item')
            print('(rep) Replace Item')
            print('(m) Exit Maintenance Mode')
            print('(q) Exit Vending Machine')

            selected_option = input('Please select an option: ').lower()

            if selected_option == 'a' or selected_option == 'rep':
                available_slots = set()

                for slot_number, slot_item in self.vending_machine.slot_items.items():
                    if slot_item is None:
                        available_slots.add(slot_number)

                selected_slot = input(f'Please select a slot number: ')

                try:
                    selected_slot_number = int(selected_slot)
                    if 0 < selected_slot_number <= self.vending_machine.total_slots:

                        replace_item = False

                        if selected_slot_number not in available_slots:
                            replace_item_response = input(
                                f'The selected slot is occupied by '
                                f'{self.vending_machine.slot_items[selected_slot_number].name}. '
                                f'Would you like to replace it? (y/n) '
                            ).lower()
                            if replace_item_response == 'y':
                                replace_item = True

                        if selected_option == 'a' or (selected_option == 'rep' and replace_item):
                            item_name = input('Please enter the name of the item to be added: ')
                            item_price = input('Please enter the price of the item to be added: ')
                            item_stock = input('Please enter the number of items to be added: ')

                            try:
                                item_price_number = float(item_price)
                            except ValueError:
                                item_price_number = None
                                print('Invalid character entered for item price! Returning to menu...')

                            try:
                                item_stock_number = int(item_stock)
                            except ValueError:
                                item_stock_number = None
                                print('Invalid character entered for item stock! Returning to menu...')

                            if type(item_price_number) is float and type(item_stock_number) is int:
                                item = Item(item_name, item_price_number, item_stock_number)

                                if selected_option == 'a':
                                    added = self.vending_machine.add_item_to_slot(
                                        selected_slot_number, item, replace=replace_item
                                    )

                                    if added:
                                        print(f'Successfully added {item_stock_number} units of {item_name} priced at '
                                              f'{item_price_number} to slot number {selected_slot_number}!')
                                    else:
                                        print(f'Could not add {item_name} to slot number {selected_slot_number}!')
                                elif selected_option == 'rep':
                                    replaced = self.vending_machine.replace_item_in_slot(selected_slot_number, item)

                                    if replaced:
                                        print(f'Successfully replaced slot number {selected_slot_number} with '
                                              f'{item_stock_number} units of {item_name} priced at '
                                              f'{item_price_number}!')
                                    else:
                                        print(f'Could not replace the item in slot number {selected_slot_number}!')
                        else:
                            if selected_slot_number not in available_slots:
                                print('Item was not replaced!')
                            else:
                                print(f'No item in {selected_slot_number} to replace!')
                    else:
                        print('Invalid slot number entered! Returning to menu...')

                except ValueError:
                    print('Invalid character entered! Returning to menu...')

            elif selected_option == 'd':
                print()
                print('==== SLOT ITEMS ====')
                for slot_number, slot_item in self.vending_machine.slot_items.items():
                    if slot_item:
                        print(f'[{slot_number}] {slot_item.name} - ${slot_item.price} (Remaining: {slot_item.stock})')
                    else:
                        print(f'[{slot_number}] Empty slot')
                print()

            elif selected_option == 'mod':
                occupied_slots = set()

                for slot_number, slot_item in self.vending_machine.slot_items.items():
                    if slot_item is not None:
                        occupied_slots.add(slot_number)

                selected_slot = input(f'Please select a slot to modify {occupied_slots}: ')

                try:
                    selected_slot_number = int(selected_slot)
                    if selected_slot_number in occupied_slots:
                        current_item = self.vending_machine.slot_items[selected_slot_number]
                        selected_suboption = ''

                        while selected_suboption != 'q':
                            print()
                            print(f'The current item in slot {selected_slot_number} has the following parameters:')
                            print(f'Name: {current_item.name}')
                            print(f'Price: {current_item.price}')
                            print(f'Stock: {current_item.stock}')
                            print()
                            print('(n) Change name')
                            print('(p) Change price')
                            print('(is) Increase stock')
                            print('(ds) Decrease stock')
                            print('(q) Return to Maintenance Mode menu')

                            selected_suboption = input('Please select a modification for this item: ')

                            if selected_suboption == 'n':
                                new_name = input('Please enter a new name for this item: ')
                                changed = self.vending_machine.change_name(selected_slot_number, new_name)

                                if changed:
                                    print(f'Successfully changed the name to {new_name}!')
                                else:
                                    print('Could not change the name!')

                            elif selected_suboption == 'p':
                                new_price = input('Please enter a new price for this item: ')

                                try:
                                    new_price_number = float(new_price)
                                    changed = self.vending_machine.change_price(selected_slot_number, new_price_number)

                                    if changed:
                                        print(f'Successfully changed the price to ${new_price_number}!')
                                    else:
                                        print('Could not change the price!')

                                except ValueError:
                                    print('Invalid character entered! Returning to submenu...')

                            elif selected_suboption == 'is':
                                increase_amount = input('Please enter an amount to increase the stock by: ')

                                try:
                                    increase_amount_number = int(increase_amount)
                                    increased, new_stock = self.vending_machine.increase_stock(
                                        selected_slot_number, increase_amount_number
                                    )

                                    if increased:
                                        print(f'Successfully increased the stock by {increase_amount_number} to '
                                              f'{new_stock}!')
                                    else:
                                        print(f'Could not increase the stock by {increase_amount_number}!')

                                except ValueError:
                                    print('Invalid character entered! Returning to submenu...')

                            elif selected_suboption == 'ds':
                                decrease_amount = input('Please enter an amount to decrease the stock by: ')

                                try:
                                    decrease_amount_number = int(decrease_amount)
                                    increased, new_stock = self.vending_machine.decrease_stock(
                                        selected_slot_number, decrease_amount_number
                                    )

                                    if increased:
                                        print(f'Successfully decreased the stock by {decrease_amount_number} to '
                                              f'{new_stock}!')
                                    else:
                                        print(f'Could not decrease the stock by {decrease_amount_number}!')

                                except ValueError:
                                    print('Invalid character entered! Returning to submenu...')
                            else:
                                if selected_suboption != 'q':
                                    print('Invalid character entered! Please try again.')

                    else:
                        print('Invalid slot number entered! Returning to menu...')

                except ValueError:
                    print('Invalid character entered! Returning to menu...')

            elif selected_option == 'mov' or selected_option == 'rem':
                occupied_slots = set()

                for slot_number, slot_item in self.vending_machine.slot_items.items():
                    if slot_item is not None:
                        occupied_slots.add(slot_number)

                source_slot = self.vending_machine.total_slots

                if selected_option == 'mov':
                    source_slot = input('Please select a slot to move: ')
                    target_slot = input('Please select a slot to move into: ')
                else:
                    target_slot = input('Please select a slot to remove: ')

                try:
                    source_slot_number = source_slot

                    if selected_option == 'mov':
                        source_slot_number = int(source_slot)

                    target_slot_number = int(target_slot)

                    if 0 < source_slot_number <= self.vending_machine.total_slots and \
                            0 < target_slot_number <= self.vending_machine.total_slots:
                        if source_slot_number in occupied_slots or selected_option != 'mov':

                            if selected_option == 'mov':
                                replace_item = False

                                if target_slot_number in occupied_slots:
                                    replace_item_response = input(
                                        f'The selected slot is occupied by '
                                        f'{self.vending_machine.slot_items[target_slot_number].name}. '
                                        f'Would you like to replace it? (y/n) '
                                    ).lower()
                                    if replace_item_response == 'y':
                                        replace_item = True

                                moved = self.vending_machine.move_item_to_slot(
                                    source_slot_number, target_slot_number, replace=replace_item
                                )

                                if moved:
                                    print(f'Successfully moved '
                                          f'{self.vending_machine.slot_items[target_slot_number].name} from slot '
                                          f'number {source_slot_number} to slot number {target_slot_number}!')
                                else:
                                    print(f'Could not move the item in slot number {source_slot_number} to '
                                          f'{target_slot_number}!')

                            elif selected_option == 'rem':
                                if target_slot_number in occupied_slots:
                                    removed = self.vending_machine.remove_item_from_slot(target_slot_number)

                                    if removed:
                                        print(f'Successfully removed item from slot number {target_slot_number}!')
                                    else:
                                        print(f'Could not remove the item in slot number {target_slot_number}!')
                                else:
                                    print('No item to remove!')

                        else:
                            print('Selected slot to move from has no item! Returning to menu...')
                    else:
                        print('Invalid slot number entered! Returning to menu...')

                except ValueError:
                    print('Invalid character entered! Returning to menu...')

            else:
                if selected_option != 'm' and selected_option != 'q':
                    print('Invalid character entered! Please try again.')

        return selected_option
