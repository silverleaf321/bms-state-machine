transitions=[
            {'trigger': 'charge', 'source': 'Idle', 'dest': 'Charging'},
            {'trigger': 'discharge', 'source': 'Idle', 'dest': 'Discharging'},
            {'trigger': 'fault', 'source': '*', 'dest': 'Fault'},
            {'trigger': 'recover', 'source': 'Fault', 'dest': 'Idle'},
            {'trigger': 'complete_charge', 'source': 'Charging', 'dest': 'Idle'},
            {'trigger': 'complete_discharge', 'source': 'Discharging', 'dest': 'Idle'} ]