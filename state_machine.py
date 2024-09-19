class BMSStateMachine:
    def __init__(self):
        self.state = 'off'
        self.voltage = 0
        self.temperature = 25  # initial temperature
        self.fault = False
        self.overcharge = False
        self.overdischarge = False
    
    def check_for_fault(self):
        # add more code here, check for short circuit
        return self.fault
    
    def check_for_extreme_temperatures(self):
        if self.temperature < 0 or self.temperature > 60:  # temperature range, change this to correct values later
            return True
        return False
    
    def check_for_overcharge(self):
        return self.overcharge
    
    def check_for_overdischarge(self):
        return self.overdischarge
    
    def handle_key_in(self):
        if self.state == 'off':
            self.state = 'key_in'
            print("key in")
            self.check_fault_and_proceed()
    
    def check_fault_and_proceed(self):
        if self.check_for_fault():
            self.state = 'off'
            print("fault detected, go to off state.")
        else:
            self.state = 'balance'
            print("no fault detected, proceed")
            self.pre_charge()
    
    def pre_charge(self):
        # precharge to 90% of total voltage
        self.voltage = 0.9 * 100  # change 100 to total voltage
        print("precharge done")
        self.state = 'idle'
        self.idle()
    
    def idle(self):
        print("In Idle state.")
        self.state = 'discharge_data_received'
        self.discharge_data_received()
    
    def discharge_data_received(self):
        print("Discharge data received.")
        if self.check_for_extreme_temperatures():
            print("extreme temperatures detected, go to off state.")
            self.state = 'off'
        elif self.check_for_fault():
            print("fault detected, go to off state.")
            self.state = 'off'
        else:
            self.state = 'balance'
            print("no faults, keep going")
            self.balance()
    
    def balance(self):
        print("Balancing the battery...")
        if self.check_for_overdischarge():
            print("overdischarge detected, go to discharge state.")
            self.state = 'discharge'
            self.discharge()
        else:
            print("battery balanced")
            self.state = 'charge'
            self.charge()
    
    def charge(self):
        print("Charging the battery...")
        if self.check_for_overcharge():
            print("overcharge detected, go to balance.")
            self.state = 'balance'
        else:
            print("charging complete, go to  off state.")
            self.state = 'off'
    
    def discharge(self):
        print("discharging battery")
        if self.check_for_fault():
            print("fault, go to off state")
            self.state = 'off'
        else:
            print("discharge complete, to to off state")
            self.state = 'off'
    
    def turn_key_off(self):
        print("key turned off, go to off state.")
        self.state = 'off'

bms = BMSStateMachine()

# key in/out
bms.handle_key_in()
bms.turn_key_off()
