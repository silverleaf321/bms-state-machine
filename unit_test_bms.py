import unittest
from state_machine import BMSStateMachine
import specs

class TestBMSStateMachine(unittest.TestCase):
    
    def setUp(self):
        # set up default bms state machine
        self.bms = BMSStateMachine()

    def test_initial_state(self):
        self.assertEqual(self.bms.state, 'off')
        self.assertEqual(self.bms.voltage, 3.6)
        self.assertEqual(self.bms.temperature, 25)
        self.assertFalse(self.bms.fault)
        self.assertFalse(self.bms.overcharge)
        self.assertFalse(self.bms.overdischarge)
        self.assertEqual(self.bms.motor_voltage, 0)
        self.assertTrue(self.bms.balanced)
        self.assertFalse(self.bms.key)

    def test_handle_key_in(self):
        self.bms.handle_key_in()
        self.assertTrue(self.bms.key)
        self.assertEqual(self.bms.state, 'idle')

    def test_turn_key_off(self):
        self.bms.handle_key_in()
        self.bms.turn_key_off()
        self.assertFalse(self.bms.key)
        self.assertEqual(self.bms.state, 'off')

    def test_check_for_fault(self):
        self.bms.check_for_fault()
        self.assertEqual(self.bms.fault, False) # ********************************
        self.assertEqual(self.bms.state, 'off')

    def test_pre_charge(self):
        self.bms.pre_charge()
        self.assertEqual(self.bms.motor_voltage, 0.9 * specs.max_tractive_system_voltage)
        self.assertEqual(self.bms.state, 'idle')

    def test_check_for_overcharge(self):
        self.bms.voltage = specs.max_voltage + 0.1  # simulate overcharge
        self.bms.check_for_overcharge()
        self.assertTrue(self.bms.overcharge)
        self.assertEqual(self.bms.state, 'balance')

    def test_check_for_overdischarge(self):
        self.bms.voltage = specs.min_voltage - 0.1  # simulate overdischarge
        self.bms.check_for_overdischarge()
        self.assertTrue(self.bms.overdischarge)
        self.assertEqual(self.bms.state, 'balance')

    def test_check_for_extreme_temperatures_discharging(self):
        self.bms.temperature = specs.min_temp_discharging - 1  # extreme low temperature
        self.bms.check_for_extreme_temperatures_discharging()
        self.assertEqual(self.bms.state, 'off')

        self.bms.temperature = specs.max_temp_discharging + 1  # extreme high temperature
        self.bms.check_for_extreme_temperatures_discharging()
        self.assertEqual(self.bms.state, 'off')

    def test_check_for_extreme_temperatures_charging(self):
        self.bms.temperature = specs.min_temp_charging - 1  # extreme low temperature for charging
        self.bms.check_for_extreme_temperatures_charging()
        self.assertEqual(self.bms.state, 'off')

        self.bms.temperature = specs.max_temp_charging + 1  # extreme high temperature for charging
        self.bms.check_for_extreme_temperatures_charging()
        self.assertEqual(self.bms.state, 'off')

    def test_discharge_data_received(self):
        self.bms.voltage = specs.min_voltage - 0.1  # simulate overdischarge
        self.bms.discharge_data_received()
        self.assertEqual(self.bms.state, 'idle')

    def test_charge_data_received(self):
        self.bms.voltage = specs.max_voltage + 0.1  # simulate overcharge
        self.bms.charge_data_recieved()
        self.assertEqual(self.bms.state, 'idle')

if __name__ == '__main__':
    unittest.main()
