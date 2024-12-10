def monitor_battery(drone):
    battery_level = drone.get_battery()
    if battery_level < 20:
        print("Battery low, returning to home...")
        drone.return_to_home()
    else:
        print(f"Battery level: {battery_level}%")
