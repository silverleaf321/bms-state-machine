import csv
from state_machine import BMSStateMachine
import specs

def load_battery_data(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def run_bms_test(simulation_data):
    bms = BMSStateMachine()
    
    index = 0
    bms.handle_key_in()
    # master key 
    while index < len(simulation_data):
        row = simulation_data[index]
        temperature = float(row['Temperature'])
        voltage = float(row['Voltage Left'])
        battery_state = row['Battery State']
        on_off = row['On Off'] == 'on'

        bms.temperature = temperature
        bms.voltage = voltage
        
        print(f"Testing with Temperature: {temperature}, Voltage: {voltage}, State: {battery_state}, On/Off: {on_off}")
        
        if battery_state != 'off':
            if on_off:
                if battery_state == 'discharging':
                    bms.discharge_data_received()
                elif battery_state == 'charging': 
                    bms.charge_data_recieved()
            else:
                bms.turn_key_off()
                return 'off'
        else:
            bms.turn_key_off()
            return 'off'

        index += 1

if __name__ == "__main__":
    print("********************************************************")
    simulation_data = load_battery_data('simulation_data.csv')
    run_bms_test(simulation_data)
