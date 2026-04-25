import subprocess

def set_fan_state(state: int):
    """
    Set fan speed state.
    0 = off
    1 = low
    2 = medium
    3 = full speed
    """
    if state not in range(4):
        raise ValueError("State must be 0, 1, 2, or 3")

    path = "/sys/class/thermal/cooling_device0/cur_state"
    with open(path, "w") as f:
        f.write(str(state))
    print(f"Fan set to state {state}")

def get_fan_state() -> int:
    path = "/sys/class/thermal/cooling_device0/cur_state"
    with open(path, "r") as f:
        return int(f.read().strip())

def set_manual_mode(manual: bool):
    """
    Switch to 'user_space' policy so the OS doesn't override your fan setting.
    Set manual=False to return to automatic control.
    """
    path = "/sys/class/thermal/thermal_zone0/policy"
    policy = "user_space" if manual else "step_wise"
    with open(path, "w") as f:
        f.write(policy)
    print(f"Thermal policy set to '{policy}'")

def get_cpu_temp() -> float:
    path = "/sys/class/thermal/thermal_zone0/temp"
    with open(path, "r") as f:
        return int(f.read().strip()) / 1000.0


if __name__ == "__main__":
    print(f"CPU Temperature: {get_cpu_temp()}°C")
    print(f"Current fan state: {get_fan_state()}")

    # Switch to manual control
    set_manual_mode(True)

    # Turn fan OFF
    set_fan_state(0)

    # Turn fan ON (full speed)
    # set_fan_state(3)

    # Return to automatic control
    # set_manual_mode(False)