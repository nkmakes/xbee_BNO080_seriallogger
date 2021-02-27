# Copyright (c) 2019, Digi International, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import xbee
from machine import (I2C, ADC)
from i2c import BNO08X_I2C
from BNO080 import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)

# BOSS 64 bit DIR
TARGET_64BIT_ADDR = b'\00\x13\xA2\x00\x41\xB8\xF1\x2B'

# Pin D3 (AD3/DIO3)
ADC_PIN_ID = "D3"

# ADC reference voltage
AV_VALUES = {0: 1.25, 1: 2.5, 2: 3.3, None: 2.5}

try:
    av = xbee.atcmd("AV")
except KeyError:
    # Reference is set to 2.5 V on XBee 3 Cellular
    av = None
reference = AV_VALUES[av]
print("Configured Analog Digital Reference: AV:{}, {} V".format(av, reference))


# Create an ADC object for pin DIO0/AD0.
adc_pin = ADC(ADC_PIN_ID)

# Create a BNO080 object
i2c_obj = I2C(1, freq=400000)
bno = BNO08X_I2C(i2c_obj, debug=False)
#bno = BNO08X_I2C(i2c_obj)


bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

while True:
    # getting ADC values
    value = adc_pin.read()
    print("- ADC value:", value)
    print("- Analog voltage [V]:", value * reference / 4095)

    """
    sleep(1)
    print("Acceleration:")
    accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
    print("")

    print("Gyro:")
    gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
    print("")

    print("Magnetometer:")
    mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
    print("")
    """

    #sleep(1)
    #print("Rotation Vector Quaternion:")
    #gyro_x, gyro_y, gyro_z = bno.gyro
    #mag_x, mag_y, mag_z = bno.magnetic
    #accel_x, accel_y, accel_z = bno.acceleration
    quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member


    """msg = (
        "%0.2f,%0.2f,%0.2f" % (gyro_x, gyro_y, gyro_z)
    )
    
    msg += (
        "!%0.2f,%0.2f,%0.2f" % (accel_x, accel_y, accel_z)
    )
    msg += (
        "!%0.2f,%0.2f,%0.2f" % (mag_x, mag_y, mag_z)
    )
    """

    # Data to send
    msg = (
        "%0.2f,%0.2f,%0.2f,%0.2f,%0.2f" % (quat_real, quat_i, quat_j, quat_k,value)
    )
    print(msg)

    # Send data to BOSS
    try:
        xbee.transmit(TARGET_64BIT_ADDR, msg)
    except Exception as e:
        print ("error sending")