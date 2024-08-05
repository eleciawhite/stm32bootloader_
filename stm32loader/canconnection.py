# Author: Elecia White
# GitHub repository: https://github.com/ewhite/stm32loader
#
# When this file is part of stm32loader, it is copyright according to that
# However, otherwise it is MIT licence.

"""
Handle FDCAN communication through python-can.

This does not offer support for toggling RESET and BOOT0.
"""


import can


filters = None # pass everything
#[
#    {"can_id": 0x0, "can_mask": 0x7FF, "extended": False},
#    {"can_id": 0x088, "can_mask": 0x7ff, "extended": False},
#]


class CANConnection:


    def __init__(self, channel, interface = 'socketcan'):
        self.bus = None
        self._timeout = 10
        self._channel = channel
        self._interface = interface



    @property
    def timeout(self):
        """Get timeout."""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout."""
        self._timeout = timeout
        self.serial_connection.timeout = timeout



    def connect(self):
        self.bus = can.interface.Bus(self._channel,
                                     self._interface,
                                     can_filters=filters,
                                     fd=True, 
                                     err_reporting=True,
                                     receive_own_messages=True, local_loopback=False)   


    def disconnect(self):
        if self.bus:
            self.bus.shutdown()
        self.bus = None

    def write(self, *args, **kwargs):
        """Write the given data to the CAN connection."""
        import pdb; pdb.set_trace()

        msg = can.Message(arbitration_id=0, data=args[0], is_extended_id=False, is_fd=True, check=True, bitrate_switch = True)
        print("Sent: {}".format(msg))
        return  self.bus.send(msg)
        #return self.serial_connection.write(*args, **kwargs)

    def read(self, *args, **kwargs):
        """Read the given amount of bytes from the serial connection."""
        message = self.bus.recv(1.0) # Timeout in seconds.
        return message
    
    def flush(self):
        for msg in self.bus:
            print(msg.data)

    def enable_reset(self, enable=True):
        return None
    def enable_boot0(self, enable=True):
        return None

    def flush_imput_buffer(self):
        message = bus.recv(1.0) # Timeout in seconds.
        return message

    def from_can_msg(self, msg: can.Message):
        # Currently 22 out of 29 bits of the extended arbitration_id are used.
        # Padding to 22 bits makes sure that priority=0 is parsed correctly.
        #
        # If number of bits is increased, priority will always parse the first two bits.
        b = f"{msg.arbitration_id:022b}"
        priority = int(b[0:2], 2)
        board_id = int(b[2:6], 2)
        command_id = int(b[6:13], 2)
        request_id = int(b[13:21], 2)
        error_flag = bool(int(b[21]))
        return priority, board_id, command_id, request_id, error_flag
