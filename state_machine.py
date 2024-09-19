from states import ChargingState, DischargingState, IdleState, FaultState
from transitions import Machine

class BatteryManagementSystem:
    def __init__(self):
        self.state_machine = Machine(model=self, states=[
            ChargingState(),
            DischargingState(),
            IdleState(),
            FaultState()
        ], transitions=[
            {'trigger': 'charge', 'source': 'Idle', 'dest': 'Charging'},
            {'trigger': 'discharge', 'source': 'Idle', 'dest': 'Discharging'},
            {'trigger': 'fault', 'source': '*', 'dest': 'Fault'},
            {'trigger': 'recover', 'source': 'Fault', 'dest': 'Idle'},
            {'trigger': 'complete_charge', 'source': 'Charging', 'dest': 'Idle'},
            {'trigger': 'complete_discharge', 'source': 'Discharging', 'dest': 'Idle'}
        ], initial='Idle')

    def charge_battery(self):
        self.charge()
        
    def discharge_battery(self):
        self.discharge()

    def trigger_fault(self):
        self.fault()

    def recover_from_fault(self):
        self.recover()

    def complete_charge(self):
        self.complete_charge()

    def complete_discharge(self):
        self.complete_discharge()
