import unittest
from state_machine import BatteryManagementSystem

class TestBatteryManagementSystem(unittest.TestCase):
    def setUp(self):
        self.bms = BatteryManagementSystem()

    def test_initial_state(self):
        self.assertEqual(self.bms.state_machine.state, 'Idle')

    def test_charge_transition(self):
        self.bms.charge_battery()
        self.assertEqual(self.bms.state_machine.state, 'Charging')

    def test_discharge_transition(self):
        self.bms.discharge_battery()
        self.assertEqual(self.bms.state_machine.state, 'Discharging')

    def test_fault_transition(self):
        self.bms.trigger_fault()
        self.assertEqual(self.bms.state_machine.state, 'Fault')

    def test_recover_from_fault(self):
        self.bms.trigger_fault()
        self.bms.recover_from_fault()
        self.assertEqual(self.bms.state_machine.state, 'Idle')

    def test_complete_charge(self):
        self.bms.charge_battery()
        self.bms.complete_charge()
        self.assertEqual(self.bms.state_machine.state, 'Idle')

    def test_complete_discharge(self):
        self.bms.discharge_battery()
        self.bms.complete_discharge()
        self.assertEqual(self.bms.state_machine.state, 'Idle')

if __name__ == '__main__':
    unittest.main()
