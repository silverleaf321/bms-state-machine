import unittest
import state_machine

class TestBMSStateMachine(unittest.TestCase):
    
    def setUp(self):
        self.bms = state_machine.BMSStateMachine()

    def test_initial_state(self):
        # initial state should be off
        self.assertEqual(self.bms.state, 'off')
    
    def test_key_in_transition(self):
        # key in key out
        self.bms.handle_key_in()
        self.assertEqual(self.bms.state, 'balance')

    def test_fault_detection_on_key_in(self):

        # key in and detects fault
        self.bms.handle_key_in()
        self.bms.fault = True
        self.assertEqual(self.bms.state, 'off')  # should stay off
    
    def test_pre_charge_state(self):
        # try precharge, no faults detected
        self.bms.handle_key_in()
        self.assertEqual(self.bms.voltage, 90)  # check that precharge is complete (up to 90% of operating voltage)
        self.assertEqual(self.bms.state, 'idle')  # check that it transitions to idle
    
    def test_discharge_data_received(self):
        # recieved discharge data ie. gas pedal is pressed
        self.bms.handle_key_in()  # car turns on, should be idle right now
        self.bms.discharge_data_received()
        self.assertEqual(self.bms.state, 'balance')  # go to balance

    def test_extreme_temperature_detection(self):
        # detect extreme temperature 
        self.bms.temperature = 65 
        self.bms.handle_key_in()
        self.bms.discharge_data_received()
        self.assertEqual(self.bms.state, 'off')  # should go back to off due to extreme temperature
    
    def test_overcharge_detection(self):
        # overcharge detection
        self.bms.handle_key_in()
        self.bms.state = 'charge'
        self.bms.overcharge = True
        self.bms.charge()
        self.assertEqual(self.bms.state, 'balance')  # balance and go back to charge
    
    def test_overdischarge_detection(self):
        # overdistarge protection
        self.bms.handle_key_in()  
        self.bms.discharge_data_received()
        self.bms.overdischarge = True
        self.bms.balance()
        self.assertEqual(self.bms.state, 'balance')  # go to balance
        #infinite loop? need a way to exit out of discharge if there's no battery left
    
    def test_fault_during_discharge(self):
        # fault during distarge
        self.bms.handle_key_in()
        self.bms.state = 'discharge'
        self.bms.fault = True
        self.bms.discharge()
        self.assertEqual(self.bms.state, 'off')  # should go to off state

    def test_key_off(self):
        # turn key off should go back to off state
        self.bms.handle_key_in()
        self.bms.turn_key_off()
        self.assertEqual(self.bms.state, 'off')

# Run the tests
if __name__ == '__main__':
    unittest.main()
