from unittest.mock import patch
from vending_machine.vending_machine import VendingMachineInterface

import unittest


class VendingMachineCustomerMenuTest(unittest.TestCase):

    def test_insert_money(self):
        interface = VendingMachineInterface()

        user_input = [
            'i',  # Select option to insert money
            '50',  # Insert $50
            '1',  # Select and vend slot 1
            'q'  # Quit
        ]

        with patch('builtins.input', side_effect=user_input):
            interface.run()

        self.assertEqual(48.75, interface.vending_machine.current_balance)
        self.assertEqual(19, interface.vending_machine.slot_items[1].stock)


class VendingMachineMaintenanceModeTest(unittest.TestCase):

    def test_add_item_to_slot_two(self):

        interface = VendingMachineInterface()

        user_input = [
            'm',  # Maintenance Mode option
            'a',  # Add Item option
            '2',  # Add to slot 2
            'Lemonade',  # Name of new item
            '2.00',  # Price of new item
            '15',  # Stock of new item
            'm',  # Exit Maintenance Mode
            'i',  # Insert Money option
            '2.25',  # Amount of money to insert
            '2',  # Vend slot 2
            'q',  # Quit
        ]

        with patch('builtins.input', side_effect=user_input):
            interface.run()

        self.assertEqual(0.25, interface.vending_machine.current_balance)
        self.assertEqual('Lemonade', interface.vending_machine.slot_items[2].name)
        self.assertEqual(2.00, interface.vending_machine.slot_items[2].price)
        self.assertEqual(14, interface.vending_machine.slot_items[2].stock)


if __name__ == '__main__':
    unittest.main()
