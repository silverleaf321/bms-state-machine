import specs

class BMSStateMachine:
    def __init__(self):
        self.state = 'off'
        self.voltage = 3.6
        self.temperature = 25  # initial temperature???
        self.fault = False
        self.overcharge = False
        self.overdischarge = False
        self.motor_voltage = 0 # ******
        self.balanced = True # *******
        self.key = False
    
    def check_for_fault(self):
        # add more code here, check for short circuit
        # how to check for short circuit? just get value?
        if self.voltage > specs.max_temp_discharging:
            self.fault = True
        else:
            self.fault = False
        return self.fault

    def check_for_voltage(self):
        if self.voltage < specs.min_voltage:
            self.voltage = 0 # set to low value
        elif self.temperature > specs.max_voltage:
            self.voltage = 100 # set to high value
    
    def check_for_extreme_temperatures_discharging(self): 
        if self.temperature < specs.min_temp_discharging or self.temperature > specs.max_temp_discharging:  
            self.state = 'off'

    def check_for_extreme_temperatures_charging(self): # test for this in unit test
        if self.temperature < specs.min_temp_charging or self.temperature > specs.max_temp_charging:
            self.state = 'off'
    
    def check_for_overcharge(self): # *******
        if self.voltage > specs.max_voltage:
            self.overcharge = True
            self.state = 'balance'
        return self.overcharge
    
    def check_for_overdischarge(self):
        if self.voltage < specs.min_voltage:
            # self.overdischarge = True
            self.state = 'balance'
        return self.overcharge
    
    def handle_key_in(self):
        self.state = 'key_in'
        self.key = True
        print("key in")
        self.check_fault_and_proceed()
        self.pre_charge()
        return self.key
    
    def turn_key_off(self):
        print("key turned off, go to off state.")
        self.state = 'off'
        self.key = False
        return self.key
        
    def check_fault_and_proceed(self):
        if self.check_for_fault():
            self.fault = True
            self.state = 'off'
            print("fault detected, go to off state.")
        else:
            self.state = 'balance'
            print("no fault detected, proceed")
            self.pre_charge()
        return self.fault
    
    def pre_charge(self):
        # precharge to 90% of total voltage
        self.motor_voltage = 0.9 *  specs.max_tractive_system_voltage
        print("precharge done")
        self.state = 'idle'
    
    def idle(self):
        print("in idle state")
        self.state = 'idle'
    
    def balance(self):
        print("Balancing the battery...")
        self.balanced = True 
    
    def charge(self):
        print("Charging the battery...")
        self.state = 'charge'
    
    def discharge(self):
        print("discharging battery")
        self.state = 'discharge'
    
    def discharge_data_received(self): 
        print("discharge data received")
        if self.check_for_extreme_temperatures_discharging():
            print("extreme temperatures detected, go to off state.")
            self.state = 'off'
            return
        elif self.check_for_fault():
            print("fault detected, go to off state.")
            self.state = 'off'
            return
        elif self.check_for_overdischarge():
            print("overdischarge detected, balance battery")
            self.state = 'balance'
            self.balanced = True
            self.state = 'idle'
            return
        else:
            print("no extreme temperatures detected")
            print("no fault detetced")
            print("no overdischarge detected")
            print("DISCHARGING")
            self.state = 'discharge'
    
    def charge_data_recieved(self):
        print("discharge data received")
        if self.check_for_extreme_temperatures_charging():
            print("extreme temperatures detected, go to off state.")
            self.state = 'off'
            return
        elif self.check_for_fault():
            print("fault detected, go to off state.")
            self.state = 'off'
            return
        elif self.check_for_overcharge():
            print("overcharge detected, balance battery")
            self.state = 'balance'
            self.balanced = True
            self.state = 'idle'
            return
        else:
            print("no extreme temperatures detected")
            print("no fault detetced")
            print("no overcharge detected")
            print("CHARGING")
            self.state = 'charge'

# bms = BMSStateMachine()

# key in/out
# bms.handle_key_in()
# bms.turn_key_off()
