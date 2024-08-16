#!/usr/bin/env python
# Authors: Ivan A-R, Floris Lambrechts
# GitHub repository: https://github.com/florisla/stm32loader
#
# This file is part of stm32loader.
#
# stm32loader is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# stm32loader is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with stm32loader; see the file LICENSE.  If not see
# <http://www.gnu.org/licenses/>.

"""Flash firmware to STM32 microcontrollers over a serial connection."""

import sys
from types import SimpleNamespace
from pathlib import Path

try:
    from progress.bar import ChargingBar as progress_bar
except ImportError:
    progress_bar = None

from stm32loader import args
from stm32loader import hexfile
from stm32loader import bootloader
from stm32loader.devices import DEVICE_FAMILIES, DeviceFlag, DeviceFamily
from stm32loader.canconnection import CANConnection


class Stm32Loader:
    """Main application: parse arguments and handle commands."""

    def __init__(self):
        """Construct Stm32Loader object with default settings."""
        self.stm32 = None
        self.configuration = SimpleNamespace()

    def debug(self, level, message):
        """Log a message to stderror if its level is low enough."""
        if self.configuration.verbosity >= level:
            print(message)

    def parse_arguments(self, arguments):
        """Parse the list of command-line arguments."""
        self.configuration = args.parse_arguments(arguments)

    def disconnect(self):
        self.stm32.connection.disconnect()

    def connect(self):
        """Connect to the bootloader UART over an RS-232 serial port."""
        serial_connection = CANConnection(self.configuration.port)
        self.debug(
            10,
            "Open port %(port)s"
            % {"port": self.configuration.port},
        )
        try:
            serial_connection.connect()
        except IOError as e:
            print(str(e) + "\n", file=sys.stderr)
            print(
                "Is the device connected and powered correctly?\n"
                "Please use the --port option to select the correct CAN port. Examples:\n"
                "  --port can0\n",
                file=sys.stderr,
            )
            sys.exit(1)

        show_progress = self._get_progress_bar(self.configuration.no_progress)

        self.stm32 = bootloader.Stm32Bootloader(
            serial_connection,
            verbosity=self.configuration.verbosity,
            show_progress=show_progress,
            device_family=self.configuration.family,
        )

        try:
            print("Activating bootloader")
            self.stm32.reset_from_system_memory()
        except bootloader.CommandError:
            print(
                "Can't init into bootloader. Ensure that BOOT0 is enabled and reset the device.",
                file=sys.stderr,
            )
            self.stm32.reset_from_flash()
            sys.exit(1)

    def perform_commands(self):
        """Run all operations as defined by the configuration."""
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        binary_data = None
        if self.configuration.write or self.configuration.verify:
            data_file_path = Path(self.configuration.data_file)
            if data_file_path.suffix == ".hex":
                binary_data = hexfile.load_hex(data_file_path)
            else:
                binary_data = data_file_path.read_bytes()
        if self.configuration.unprotect:
            try:
                self.stm32.readout_unprotect()
            except bootloader.CommandError:
                self.debug(0, "Flash readout unprotect failed")
                self.debug(0, "Quit")
                self.stm32.reset_from_flash()
                sys.exit(1)
        if self.configuration.protect:
            try:
                self.stm32.readout_protect()
            except bootloader.CommandError:
                self.debug(0, "Flash readout protect failed")
                self.debug(0, "Quit")
                self.stm32.reset_from_flash()
                sys.exit(1)
        if self.configuration.erase:
            try:
                if self.configuration.length is None:
                    # Erase full device.
                    self.debug(0, "Performing full erase...")
                    self.stm32.erase_memory(pages=None)
                else:
                    # Erase from address to address + length.
                    start_address = self.configuration.address
                    end_address = self.configuration.address + self.configuration.length
                    pages = self.stm32.pages_from_range(start_address, end_address)
                    self.debug(0, f"Performing partial erase (0x{start_address:X} - 0x{end_address:X}, {len(pages)} pages)... ")
                    self.stm32.erase_memory(pages)

            except bootloader.CommandError:
                # may be caused by readout protection
                self.debug(
                    0,
                    "Erase failed -- probably due to readout protection.\n"
                    "Consider using the --unprotect option.",
                )
                self.stm32.reset_from_flash()
                sys.exit(1)
        if self.configuration.write:
            self.stm32.write_memory_data(self.configuration.address, binary_data)
        if self.configuration.verify:
            read_data = self.stm32.read_memory_data(self.configuration.address, len(binary_data))
            try:
                bootloader.Stm32Bootloader.verify_data(read_data, binary_data)
                print("Verification OK")
            except bootloader.DataMismatchError as e:
                print("Verification FAILED: %s" % e, file=sys.stderr)
                sys.exit(1)
        if not self.configuration.write and self.configuration.read:
            read_data = self.stm32.read_memory_data(
                self.configuration.address, self.configuration.length
            )
            with open(self.configuration.data_file, "wb") as out_file:
                out_file.write(read_data)
        if self.configuration.go_address is not None:
            self.stm32.go(self.configuration.go_address)

    def reset(self):
        """Reset the microcontroller."""
        self.stm32.reset_from_flash()

    def detect_device(self):
        boot_version = self.stm32.get()
        self.debug(0, "Bootloader version: 0x%X" % boot_version)
        self.stm32.detect_device()
        if self.stm32.device.bootloader_id is not None:
            self.debug(5, f"Bootloader ID: 0x{self.stm32.device.bootloader_id:02X}")
        self.debug(0, f"Chip ID: 0x{self.stm32.device.product_id:03X}")
        self.debug(0, f"Chip model: {self.stm32.device.device_name}")

    def read_device_uid(self):
        """Show chip UID."""
        try:
            device_uid = self.stm32.get_uid()
        except bootloader.CommandError as e:
            self.debug(
                0,
                "Something was wrong with reading chip UID: " + str(e),
            )
            return

        if device_uid != bootloader.Stm32Bootloader.UID_NOT_SUPPORTED:
            device_uid_string = self.stm32.format_uid(device_uid)
            self.debug(0, "Device UID: %s" % device_uid_string)

    def read_flash_size(self):
        """Show chip flash size."""
        try:
            flash_size = self.stm32.get_flash_size()
        except bootloader.CommandError as e:
            self.debug(
                0,
                "Something was wrong with reading chip flash size: " + str(e),
            )
            return

        if flash_size != bootloader.Stm32Bootloader.FLASH_SIZE_UNKNOWN:
            self.debug(0, f"Flash size: {flash_size} kiB")

    @staticmethod
    def _get_progress_bar(no_progress=False):
        if no_progress or not progress_bar:
            return None

        return bootloader.ShowProgress(progress_bar)


def main(*arguments, **kwargs):
    """
    Parse arguments and execute tasks.

    Default usage is to supply *sys.argv[1:].
    """
    try:
        loader = Stm32Loader()
        loader.parse_arguments(arguments)
        loader.connect()

        try:
            loader.detect_device()
            loader.read_device_uid()
            loader.read_flash_size()
            loader.perform_commands()
        finally:
            loader.reset()
    except SystemExit:
        if not kwargs.get("avoid_system_exit", False):
            raise
    finally: 
        loader.disconnect()


if __name__ == "__main__":
    main(*sys.argv[1:])
