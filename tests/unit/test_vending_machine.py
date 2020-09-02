from unittest.mock import MagicMock, patch
from vending_machine.vending_machine import Item, VendingMachine

import requests
import unittest


class VendingMachineTestCase(unittest.TestCase):

    def test_add_item_to_slot_already_occupied_with_other_item(self):
        sparkling_water = Item('Sparkling Water', 1.25, 6)
        regular_water = Item('Water', 1.00, 2)

        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, sparkling_water)
        added = vending_machine.add_item_to_slot(1, regular_water)

        self.assertFalse(added)
        self.assertEqual(8, vending_machine.available_slots)
        self.assertNotEqual('Water', vending_machine.slot_items[1].name)
        self.assertIsNotNone(vending_machine.slot_items[1])

    def test_add_item_to_slot_already_occupied_with_other_item_replace(self):
        sparkling_water = Item('Sparkling Water', 1.25, 6)
        regular_water = Item('Water', 1.00, 2)

        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, sparkling_water)
        added = vending_machine.add_item_to_slot(1, regular_water, replace=True)

        self.assertTrue(added)
        self.assertEqual(8, vending_machine.available_slots)
        self.assertEqual('Water', vending_machine.slot_items[1].name)
        self.assertIsNotNone(vending_machine.slot_items[1])

    def test_add_item_to_slot_already_occupied_with_same_item(self):
        sparkling_water = Item('Sparkling Water', 1.25, 6)

        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, sparkling_water)

        sparkling_water2 = Item('Sparkling Water', 1.5, 21)
        added = vending_machine.add_item_to_slot(1, sparkling_water2, replace=True)

        self.assertTrue(added)
        self.assertEqual(8, vending_machine.available_slots)
        self.assertEqual('Sparkling Water', vending_machine.slot_items[1].name)
        self.assertEqual(1.5, vending_machine.slot_items[1].price)
        self.assertEqual(27, vending_machine.slot_items[1].stock)

    def test_add_item_to_slot_invalid_slot(self):
        sparkling_water = Item('Sparkling Water', 1.25, 6)

        vending_machine = VendingMachine()
        added = vending_machine.add_item_to_slot(10, sparkling_water)

        self.assertFalse(added)
        self.assertEqual(9, vending_machine.available_slots)
        self.assertEqual('Invalid slot', vending_machine.slot_items.get(10, 'Invalid slot'))

    def test_add_item_to_slot_success(self):
        sparkling_water = Item('Sparkling Water', 1.25, 6)

        vending_machine = VendingMachine()
        added = vending_machine.add_item_to_slot(1, sparkling_water)

        self.assertTrue(added)
        self.assertEqual(8, vending_machine.available_slots)
        self.assertEqual('Sparkling Water', vending_machine.slot_items[1].name)
        self.assertEqual(1.25, vending_machine.slot_items[1].price)
        self.assertEqual(6, vending_machine.slot_items[1].stock)

    def test_remove_item_from_slot_no_items(self):
        vending_machine = VendingMachine()
        removed = vending_machine.remove_item_from_slot(1)

        self.assertFalse(removed)
        self.assertEqual(9, vending_machine.available_slots)
        self.assertIsNone(vending_machine.slot_items[1])

    def test_remove_item_from_slot_invalid_slot(self):
        vending_machine = VendingMachine()
        removed = vending_machine.remove_item_from_slot(11)

        self.assertFalse(removed)
        self.assertEqual(9, vending_machine.available_slots)
        self.assertEqual('Invalid slot', vending_machine.slot_items.get(11, 'Invalid slot'))

    def test_remove_item_from_slot_success(self):
        sparkling_water = Item('Sparkling Water', 1.25, 6)

        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, sparkling_water)
        removed = vending_machine.remove_item_from_slot(1)

        self.assertTrue(removed)
        self.assertEqual(9, vending_machine.available_slots)
        self.assertIsNone(vending_machine.slot_items[1])

    def test_insert_money_negative_amount(self):
        vending_machine = VendingMachine()
        inserted, total_balance = vending_machine.insert_money(-21.65)

        self.assertFalse(inserted)
        self.assertEqual(0, total_balance)

    def test_insert_money_success(self):
        vending_machine = VendingMachine()
        inserted, total_balance = vending_machine.insert_money(12)

        self.assertTrue(inserted)
        self.assertEqual(12, total_balance)

        inserted, total_balance = vending_machine.insert_money(53.5)

        self.assertTrue(inserted)
        self.assertEqual(65.5, total_balance)

    def test_remove_money_negative_amount(self):
        vending_machine = VendingMachine()
        removed, total_balance = vending_machine.remove_money(-124)

        self.assertFalse(removed)

    def test_remove_money_empty_balance(self):
        vending_machine = VendingMachine()
        removed, total_balance = vending_machine.remove_money(89)

        self.assertFalse(removed)

    def test_remove_money_amount_higher_than_balance(self):
        vending_machine = VendingMachine()
        inserted, total_balance = vending_machine.insert_money(23)
        removed, total_balance_after_removal = vending_machine.remove_money(total_balance * 2)

        self.assertTrue(removed)
        self.assertEqual(0, total_balance_after_removal)

    def test_remove_money_success(self):
        vending_machine = VendingMachine()
        vending_machine.insert_money(238)
        removed, total_balance = vending_machine.remove_money(213)

        self.assertTrue(removed)
        self.assertEqual(25, total_balance)

    def test_select_and_vend_invalid_slot(self):
        vending_machine = VendingMachine()
        vended, item_summary, vend_result, total_balance = vending_machine.select_and_vend(10)

        self.assertFalse(vended)
        self.assertEqual('', item_summary)
        self.assertEqual('Invalid Slot', vend_result)

    def test_select_and_vend_empty_slot(self):
        vending_machine = VendingMachine()
        vended, item_summary, vend_result, total_balance = vending_machine.select_and_vend(1)

        self.assertFalse(vended)
        self.assertEqual('', item_summary)
        self.assertEqual('Empty Slot', vend_result)

    @patch('vending_machine.vending_machine.VendingMachine._get_abstract', MagicMock(return_value='Sparkling Water'))
    def test_select_and_vend_not_enough_money(self):
        sparkling_water = Item('Sparkling Water', 1.25, 6)

        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, sparkling_water)
        vended, item_summary, vend_result, total_balance = vending_machine.select_and_vend(1)

        self.assertFalse(vended)
        self.assertEqual('Sparkling Water', item_summary)
        self.assertEqual('Insufficient Balance', vend_result)

    @patch('vending_machine.vending_machine.VendingMachine._get_abstract', MagicMock(return_value='Orange Juice'))
    def test_select_and_vend_out_of_stock(self):
        orange_juice = Item('Orange Juice', 1.50, 0)

        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, orange_juice)
        vending_machine.insert_money(12)
        vended, item_summary, vend_result, total_balance = vending_machine.select_and_vend(1)

        self.assertFalse(vended)
        self.assertEqual('Orange Juice', item_summary)
        self.assertEqual('Out of Stock', vend_result)

    @patch('vending_machine.vending_machine.VendingMachine._get_abstract', MagicMock(return_value='Soda'))
    def test_select_and_vend_success(self):
        soda = Item('Soda', 1.25, 20)

        vending_machine = VendingMachine()
        vending_machine.insert_money(10.0)
        vending_machine.add_item_to_slot(3, soda)
        vended, item_summary, vend_result, total_balance = vending_machine.select_and_vend(3)

        self.assertTrue(vended)
        self.assertEqual('Soda', item_summary)
        self.assertEqual('Vended: Soda', vend_result)
        self.assertEqual(8.75, total_balance)

    def test_get_abstract_request_exception(self):
        vending_machine = VendingMachine()

        with patch('requests.get', MagicMock(side_effect=requests.exceptions.RequestException)):
            self.assertEqual('', vending_machine._get_abstract('test'))

    def test_get_abstract_success(self):
        vending_machine = VendingMachine()

        with patch('requests.models.Response.json', MagicMock(return_value={'AbstractText': ''})):
            self.assertEqual('', vending_machine._get_abstract('test'))

        with patch('requests.models.Response.json', MagicMock(return_value={'AbstractText': 'Test text'})):
            self.assertEqual('Test text', vending_machine._get_abstract('test'))

    def test_move_item_to_slot_invalid_source_slot(self):
        self.assertFalse(VendingMachine().move_item_to_slot(11, 1))

    def test_move_item_to_slot_invalid_target_slot(self):
        self.assertFalse(VendingMachine().move_item_to_slot(1, 11))

    def test_move_item_to_slot_empty_source_slot(self):
        self.assertFalse(VendingMachine().move_item_to_slot(1, 2))

    def test_move_item_to_slot_empty_target_slot(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Soda', 1.25, 20))

        self.assertTrue(vending_machine.move_item_to_slot(1, 2))
        self.assertIsNone(vending_machine.slot_items[1])
        self.assertEqual('Soda', vending_machine.slot_items[2].name)

    def test_move_item_to_same_slot(self):
        self.assertFalse(VendingMachine().move_item_to_slot(1, 1))

    def test_move_item_to_slot_target_slot_has_item(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Soda', 1.25, 20))
        vending_machine.add_item_to_slot(2, Item('Coffee', 1.75, 6))

        self.assertFalse(vending_machine.move_item_to_slot(1, 2))
        self.assertEqual('Soda', vending_machine.slot_items[1].name)
        self.assertEqual('Coffee', vending_machine.slot_items[2].name)

    def test_move_item_to_slot_replace_item_in_target_slot(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Soda', 1.25, 20))
        vending_machine.add_item_to_slot(2, Item('Coffee', 1.75, 6))

        self.assertTrue(vending_machine.move_item_to_slot(1, 2, replace=True))
        self.assertIsNone(vending_machine.slot_items[1])
        self.assertEqual('Soda', vending_machine.slot_items[2].name)

    def test_replace_item_in_slot_invalid_slot(self):
        self.assertFalse(VendingMachine().replace_item_in_slot(12, Item('Soda', 1.25, 20)))

    def test_replace_item_in_slot_empty_slot(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Coffee', 1.75, 6))
        self.assertTrue(vending_machine.replace_item_in_slot(1, Item('Soda', 1.25, 20)))
        self.assertTrue(8, vending_machine.available_slots)

    def test_replace_item_in_slot_success(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Coffee', 1.75, 6))
        self.assertTrue(vending_machine.replace_item_in_slot(1, Item('Soda', 1.25, 20)))

    def test_change_name_invalid_slot(self):
        self.assertFalse(VendingMachine().change_name(15, 'Iced Tea'))

    def test_change_name_empty_slot(self):
        self.assertFalse(VendingMachine().change_name(1, 'Iced Tea'))

    def test_change_name_success(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Coffee', 1.75, 6))

        self.assertTrue(vending_machine.change_name(1, 'Iced Tea'))
        self.assertEqual('Iced Tea', vending_machine.slot_items[1].name)

    def test_change_price_invalid_slot(self):
        self.assertFalse(VendingMachine().change_price(15, 2.25))

    def test_change_price_empty_slot(self):
        self.assertFalse(VendingMachine().change_price(1, 2.25))

    def test_change_price_success(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Coffee', 1.75, 6))

        self.assertTrue(vending_machine.change_price(1, 2.25))
        self.assertEqual(2.25, vending_machine.slot_items[1].price)

    def test_increase_stock_invalid_slot(self):
        increased, new_stock = VendingMachine().increase_stock(15)
        self.assertFalse(increased)

    def test_increase_stock_empty_slot(self):
        increased, new_stock = VendingMachine().increase_stock(1)
        self.assertFalse(increased)

    def test_increase_stock_success(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Coffee', 1.75, 6))
        increased, new_stock = vending_machine.increase_stock(1, 15)

        self.assertTrue(increased)
        self.assertEqual(21, new_stock)
        self.assertEqual(21, vending_machine.slot_items[1].stock)

    def test_decrease_stock_invalid_slot(self):
        decreased, new_stock = VendingMachine().decrease_stock(13)
        self.assertFalse(decreased)

    def test_decrease_stock_empty_slot(self):
        decreased, new_stock = VendingMachine().decrease_stock(1)
        self.assertFalse(decreased)

    def test_decrease_stock_amount_higher_than_current_stock(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Coffee', 1.75, 6))
        decreased, new_stock = vending_machine.decrease_stock(1, 25)

        self.assertTrue(decreased)
        self.assertEqual(0, new_stock)
        self.assertEqual(0, vending_machine.slot_items[1].stock)

    def test_decrease_stock_amount_success(self):
        vending_machine = VendingMachine()
        vending_machine.add_item_to_slot(1, Item('Coffee', 1.75, 6))
        decreased, new_stock = vending_machine.decrease_stock(1, 4)

        self.assertTrue(decreased)
        self.assertEqual(2, new_stock)
        self.assertEqual(2, vending_machine.slot_items[1].stock)


if __name__ == '__main__':
    unittest.main()
