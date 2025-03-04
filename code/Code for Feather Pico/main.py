import board
import microcontroller
import digitalio
from analogio import AnalogIn
from joystick_xl.inputs import Axis
from joystick_xl.inputs import Button
from joystick_xl.joystick import Joystick

# Setup LED and Button
led = digitalio.DigitalInOut(board.D24)
led.direction = digitalio.Direction.OUTPUT
button = digitalio.DigitalInOut(board.D25)
button.switch_to_input(pull=digitalio.Pull.UP)

# Define axis configuration constants
AXIS_DB1 = 10  # Deadband to apply to axis center points.
AXIS_DB2 = 100
AXIS_MIN = 0  # Minimum raw axis value.
AXIS_MAX = 65535  # Maximum raw axis value.

# Create Joystick instance
joystick = Joystick()

# Create AnalogIn instances for analog inputs
analog_z_button = AnalogIn(board.A2)
analog_z_no_button = AnalogIn(board.A3)
flip_x = AnalogIn(board.A1)
flip_y = AnalogIn(board.A0)

# Add an Axis to the joystick with specified deadband and range with the board pin defined, these become "hardcoded" and you cant mess with them. if defined like the z axis, you can mess with them in code
# if you need access to special pins that are reserved as something aside from digitalio like the MOSI, and MISO pins you can call for them using the microcontroller.pin.gpio# decleration to call them as digitalio
joystick.add_input(
    Button(board.D5),  #1
    Button(board.D6),  #2
    Button(microcontroller.pin.GPIO20), #3
    Button(board.D10),  #4
    Button(),  #5
    Button(board.D12),  #6
    Button(board.D1),  #7
    Button(board.D0),  #8
    Button(board.D9),  #9
    Button(board.D4),  #10
    Button(),  #11
    Button(board.D11),  #12
    Axis(deadband=AXIS_DB2, min=AXIS_MIN, max=AXIS_MAX),
    Axis(deadband=AXIS_DB2, min=AXIS_MIN, max=AXIS_MAX),
    Axis(),
    Axis(),
    Axis(),
    Axis(deadband=AXIS_DB1, min=AXIS_MIN, max=AXIS_MAX)

)

def map_value(raw_value, in_min, in_max, out_min, out_max):
    """
    Map the input value from one range to another.

    Parameters:
    - raw_value: The raw input value to be mapped.
    - in_min: Minimum value of the input range.
    - in_max: Maximum value of the input range.
    - out_min: Minimum value of the output range.
    - out_max: Maximum value of the output range.

    Returns:
    - Mapped value within the specified output range.

    Additional notes:
    if you invert the out_min and out_max values this will invert the axis inputs
    """
    # Map the input value using a linear mapping formula
    return int((raw_value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    led.value = button.value
    

    if button.value:
        # Map analog_x_button value within the specified range
        z_value = map_value(analog_z_button.value, 0, 65535, 0,  65535 )
    else:
        # Use raw analog_x_no_button value when the button is not pressed
        z_value = analog_z_no_button.value

    # Ensure the mapped value is an integer
    z_mapped = int(z_value)
    x_flipped = int(map_value(flip_x.value, 65535, 0, 0,  65535 ))
    y_flipped = int(map_value(flip_y.value, 65535, 0, 0,  65535 ))
    # Update the joystick axis with the mapped value
    joystick.axis[0].source_value = x_flipped
    joystick.axis[1].source_value = y_flipped
    joystick.axis[5].source_value = z_mapped
    joystick.update()

    # Add more logic for buttons, triggers, etc.
