from transitions import State

class ChargingState(State):
    def on_enter(self):
        print("Entering Charging State")

class DischargingState(State):
    def on_enter(self):
        print("Entering Discharging State")

class IdleState(State):
    def on_enter(self):
        print("Entering Idle State")

class FaultState(State):
    def on_enter(self):
        print("Entering Fault State")
