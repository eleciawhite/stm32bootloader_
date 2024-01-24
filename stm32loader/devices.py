import enum


@enum.unique
class DeviceFamily(enum.Enum):
    # AN2606
    C0 = "C0"
    F0 = "F0"
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F7 = "F7"
    G0 = "G0"
    G4 = "G4"
    H5 = "H5"
    H7 = "H7"
    L0 = "L0"
    L1 = "L1"
    L4 = "L4"
    L5 = "L5"
    WBA = "WBA"
    WB = "WB"
    WL = "WL"
    U5 = "U5"
    # Not sure if these really exist?
    W = "W"

    # Non-STM devices.
    NRG = "NRG"
    WIZ = "WIZ"


@enum.unique
class DeviceFlag(enum.IntEnum):
    NONE = 0
    OBL_LAUNCH = 1
    CLEAR_PEMPTY = 2
    # For some reason, F4 (at least, NUCLEO F401RE) can't read the 12 or 2
    # bytes for UID and flash size directly.
    # Reading a whole chunk of 256 bytes at 0x1FFFA700 does work and
    # requires some data extraction.
    LONG_UID_ACCESS = 8,
    FORCE_PARITY_NONE = 16


class DeviceFamilyInfo:

    def __init__(
            self,
            name,
            uid_address=None,
            flash_size_address=None,
            flash_page_size=1024,
            transfer_size=256,
            mass_erase=True,
            option_bytes=None,
            bootloader_id_address=None,
            flags=DeviceFlag.NONE,
    ):
        self.name = name
        self.uid_address = uid_address
        self.flash_size_address = flash_size_address
        self.flash_page_size = flash_page_size
        self.transfer_size = transfer_size
        self.mass_erase = mass_erase
        self.option_bytes = option_bytes
        self.bootloader_id_address = bootloader_id_address
        self.family_default_flags = flags


DEVICE_FAMILIES = {
    DeviceFamily.C0: DeviceFamilyInfo("C0", bootloader_id_address=0x_1FFF_17FE),
    # RM0360
    DeviceFamily.F0: DeviceFamilyInfo("F0", flash_size_address=0x_1FFF_F7CC, option_bytes=(0x_1FFF_F800, 0x_1FFF_F80F)),
    # RM0008
    DeviceFamily.F1: DeviceFamilyInfo("F1", uid_address=0x_1FFF_F7E8, flash_size_address=0x_1FFF_F7E0, option_bytes=(0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceFamily.F2: DeviceFamilyInfo("F2", option_bytes=(0x_1FFF_C000, 0x_1FFF_C00F), bootloader_id_address=0x_1FFF_77DE),
    # RM0366, RM0365, RM0316, RM0313, RM4510
    DeviceFamily.F3: DeviceFamilyInfo("F3", uid_address=0x_1FFF_F7AC, flash_size_address=0x_1FFF_F7CC, flash_page_size=2048, bootloader_id_address=0x_1FFF_F796),
    # RM0090
    DeviceFamily.F4: DeviceFamilyInfo("F4", uid_address=0x_1FFF_7A10, flash_size_address=0x_1FFF_7A22, bootloader_id_address=0x_1FFF_76DE, flags=DeviceFlag.LONG_UID_ACCESS),
    # RM0385
    DeviceFamily.F7: DeviceFamilyInfo("F7", uid_address=0x_1FF0_F420, flash_size_address=0x_1FF0_F442, bootloader_id_address=0x_1FF0_EDBE),
    # RM0444
    DeviceFamily.G0: DeviceFamilyInfo("G0", uid_address=0x_1FFF_7590, flash_size_address=0x_1FFF_75E0),
    DeviceFamily.G4: DeviceFamilyInfo("G4", bootloader_id_address=0x_1FFF_6FFE),
    DeviceFamily.H5: DeviceFamilyInfo("H5", ),
    # RM0433
    DeviceFamily.H7: DeviceFamilyInfo("H7", uid_address=0x_1FF1_E800, flash_size_address=0x_1FF1_E880, flash_page_size=128 * 1024),
    # FIXME TWO RMs?
    # RM0451, RM4510
    DeviceFamily.L0: DeviceFamilyInfo("L0", uid_address=0x_1FF8_0050, flash_size_address=0x_1FF8_007C, transfer_size=128, flash_page_size=128, mass_erase=False, flags=DeviceFlag.LONG_UID_ACCESS),
    DeviceFamily.L1: DeviceFamilyInfo("L1", mass_erase=False),
    # RM0394
    DeviceFamily.L4: DeviceFamilyInfo("L4", uid_address=0x_1FFF_7590, flash_size_address=0x_1FFF_75E0, bootloader_id_address=0x_1FFF_6FFE),
    DeviceFamily.L5: DeviceFamilyInfo("L5", ),
    DeviceFamily.WBA: DeviceFamilyInfo("WBA", ),
    DeviceFamily.WB: DeviceFamilyInfo("WB", ),
    # RM0453
    DeviceFamily.WL: DeviceFamilyInfo("WL", uid_address=0x_1FFF_7590, flash_size_address=0x_1FFF_75E0),
    DeviceFamily.U5: DeviceFamilyInfo("U5", ),
    DeviceFamily.W: DeviceFamilyInfo("W", ),
    # ST BlueNRG series; see ST AN4872 (BlueNRG-1/2) and AN5471 (BlueNRG-LP/LPS). BlueNRG requires parity 'none'.
    #   Product ID:
    #       Byte 1: metal fix (masked out)
    #       Byte 2: mask set (masked out)
    #       Byte 3: 0xHL
    #           H: [0] BlueNRG-1, [2] BlueNRG-2, [3] BlueNRG-LP/LPS
    #           L: [3] 160kB, [B] 192kB, [F] 256kB
    #   There is no access to peripherals/system memory from bootloader, so flash size and UID can not be read
    #       NRG-1/2: flash_size_address=0x_4010_0014, uid_address=0x_1000_07F4
    #       NRG-LP:  flash_size_address=0x_4000_1014, uid_address=0x_1000_1EF0
    DeviceFamily.NRG: DeviceFamilyInfo("NRG", flags=DeviceFlag.FORCE_PARITY_NONE, flash_page_size=2048),
    DeviceFamily.WIZ: DeviceFamilyInfo("WIZ", ),
}


kB = 1024


class Flash:

    # RM0090 4 sectors of 16 Kbytes, 1 sector of 64 Kbytes, 7 sectors of 128 Kbytes
    F2_F4_PAGE_SIZE = (16 * kB, 16 * kB, 16 * kB, 16 * kB, 64 * kB, 128 * kB, 0)
    # RM0090 4 sectors of 16 Kbytes, 1 sector of 64 Kbytes, 7 sectors of 128 Kbytes... per bank
    F4_DUAL_BANK_PAGE_SIZE = (
        16 * kB, 16 * kB, 16 * kB, 16 * kB, 64 * kB, 128 * kB, 128 * kB, 128 * kB, 128 * kB,
        16 * kB, 16 * kB, 16 * kB, 16 * kB, 64 * kB, 128 * kB, 0,
    )
    F7_PAGE_SIZE = (32 * kB, 32 * kB, 32 * kB, 32 * kB, 128 * kB, 256 * kB, 0)

    def __init__(self, start=None, end=None, page_size=None, pages_per_sector=None):
        self.start = start
        self.end = end
        self.page_size = page_size
        self.pages_per_sector = pages_per_sector

    @property
    def size(self):
        if self.start is None:
            return 0

        return self.end - self.start


class DeviceInfo:

    def __init__(self, device_family, device_name, pid, bid, variant=None, line=None, ram=None, flash=None, system=None, option=None, bootloader_id_address=None, flags=DeviceFlag.NONE):
        self.family = DEVICE_FAMILIES[DeviceFamily[device_family]]
        self.device_name = device_name
        self.product_id = pid
        self.bootloader_id = bid
        self.variant = variant
        self.product_line = line
        self.ram = ram
        self.flash = Flash(*(flash or []))
        self.system_memory = system
        self.option_bytes = option
        self.flags = flags | self.family.family_default_flags
        self.bootloader_id_address = bootloader_id_address or self.family.bootloader_id_address

    @property
    def ram_size(self):
        if self.ram is None:
            return 0

        assert isinstance(self.ram, tuple)

        if isinstance(self.ram[0], tuple):
            # Multiple ranges.
            ram_size = 0
            for ram_range in self.ram:
                ram_size += ram_range[1] - ram_range[0]

            return ram_size

        start, end = self.ram
        ram_size = end - start
        return ram_size

    @property
    def flash_size(self):
        return self.flash.size

    @property
    def system_memory_size(self):
        if self.system_memory is None:
            return 0

        assert isinstance(self.system_memory, tuple)

        if isinstance(self.system_memory[0], tuple):
            # Multiple ranges.
            flash_size = 0
            for flash_range in self.system_memory:
                flash_size += flash_range[1] - flash_range[0]

            return flash_size

        start, end = self.system_memory
        flash_size = end - start
        return flash_size

    def __str__(self):
        name = self.device_name
        if self.variant:
            name += f"-{self.variant}"
        if self.product_line:
            name += f"-{self.product_line}"
        return name

    def __repr__(self):
        return f"DeviceInfo(device_name={self.device_name!r}, variant={self.product_line!r})"


@enum.unique
class BootloaderSerialPeripherals(enum.Enum):
    # AN2606
    USART = 1
    DUAL_USART = 2
    UART_CAN_DFU = 3
    USART_DFU = 4
    USART_I2C = 5
    I2C = 6
    I2C_CAN_DFU_I2C = 7
    I2C_SPI = 8
    USART_CAN_FDCAN_DFU_I2C_SPI = 9
    USART_DFU_FDCAN_SPI = 10
    USART_I2C_SPI = 11
    USART_SPI = 12
    USART_DFU_I2C_SPI = 13
    USART_DFU_I2C_I3C_FDCAN_SPI = 14


DEVICE_DETAILS = [
    # Based on ST AN2606 section "Device-dependent bootloader parameters".
    # Flash range, option bytes and flags gleaned from stm32flash, dev_table.c.

    # FIXME flash?
    DeviceInfo("C0", "STM32C011xx", 0x443, 0x51, ram=(0x_2000_0000, 0x_2000_3000), system=(0x_1FFF_0000, 0x_1FFF_1800), flash=None, option=None),
    # FIXME flash?
    # Error in AN2606? Ram is mentioned as 0x_2000_2000 - 0x_2000_17FF
    DeviceInfo("C0", "STM32C031xx", 0x453, 0x52, ram=(0x_2000_2000, 0x_2000_2800), system=(0x_1FFF_0000, 0x_1FFF_1800), flash=None, option=None),
    DeviceInfo("F0", "STM32F05xxx/030x8", 0x440, 0x21, ram=(0x_2000_0800, 0x_2000_2000), system=(0x_1FFF_EC00, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0801_0000, 1 * kB, 4), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F7A6),
    DeviceInfo("F0", "STM32F03xx4/6", 0x444, 0x10, ram=(0x_2000_0800, 0x_2000_1000), system=(0x_1FFF_EC00, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0800_8000, 1 * kB, 4), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F7A6),
    # FIXME different flash size for both devices with PID=0x442 ?
    DeviceInfo("F0", "STM32F030xC", 0x442, 0x52, ram=(0x_2000_1800, 0x_2000_8000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F796, flags=DeviceFlag.OBL_LAUNCH),
    # FIXME different flash size for both devices with PID=0x445 ?
    DeviceInfo("F0", "STM32F04xxx", 0x445, 0xA1, ram=None, system=(0x_1FFF_C400, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0800_8000, 1 * kB, 4), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F6A6),
    DeviceInfo("F0", "STM32F070x6", 0x445, 0xA2, ram=None, system=(0x_1FFF_C400, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0800_8000, 1 * kB, 4), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F6A6),
    # FIXME different flash size for both devices with PID=0x448 ?
    DeviceInfo("F0", "STM32F070xB", 0x448, 0xA3, ram=(0x_1FFF_C800, 0x_1FFF_F800), system=None, flash=(0x_0800_0000, 0x_0802_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F6A6),
    DeviceInfo("F0", "STM32F071xx/072xx", 0x448, 0xA1, ram=(0x_2000_1800, 0x_2000_4000), system=(0x_1FFF_C800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0802_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F6A6),
    DeviceInfo("F0", "STM32F09xxx", 0x442, 0x50, ram=(0x_1FFF_D800, 0x_1FFF_F800), system=None, flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F796, flags=DeviceFlag.OBL_LAUNCH),
    DeviceInfo("F1", "STM32F10xxx", line="Low-density",  pid=0x412, bid=None, ram=(0x_2000_0200, 0x_2000_2800), system=(0x_1FFF_F000, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0800_8000, 1 * kB, 4), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F1", "STM32F10xxx", line="Medium-density",  pid=0x410, bid=None, ram=(0x_2000_0200, 0x_2000_5000), system=(0x_1FFF_F000, 0x_1FFF_F800), flash = (0x_0800_0000, 0x_0802_0000, 1 * kB, 4), option = (0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F1", "STM32F10xxx", line="High-density",  pid=0x414, bid=None, ram=(0x_2000_0200, 0x_2001_0000), system=(0x_1FFF_F000, 0x_1FFF_F800), flash = (0x_0800_0000, 0x_0808_0000, 2 * kB, 2), option = (0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F1", "STM32F10xxx", line="Medium-density value", pid=0x420, bid=0x10, ram=(0x_2000_0200, 0x_2000_2000), system=(0x_1FFF_F000, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0802_0000, 1 * kB, 4), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F7D6),
    DeviceInfo("F1", "STM32F10xxx", line="High-density value", pid=0x428, bid=0x10, ram=(0x_2000_0200, 0x_2000_8000), system=(0x_1FFF_F000, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F7D6),
    DeviceInfo("F1", "STM32F105xx/107xx", line="Connectivity", pid=0x418, bid=None, ram=(0x_2000_1000, 0x_2001_0000), system=(0x_1FFF_B000, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F1", "STM32F10xxx", line="XL-density", pid=0x430, bid=0x21, ram=(0x_2000_0800, 0x_2001_8000), system=(0x_1FFF_E000, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0810_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F7D6),
    # FIXME different flash size for both devices with PID=0x411 ?
    DeviceInfo("F2", "STM32F2xxxx", 0x411, 0x20, ram=(0x_2000_2000, 0x_2002_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0810_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F2", "STM32F2xxxx", 0x411, 0x33, ram=(0x_2000_2000, 0x_2002_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0810_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    # FIXME different flash size for both devices with PID=0x432 ?
    DeviceInfo("F3", "STM32F373xx", 0x432, 0x41, ram=(0x_2000_1400, 0x_2000_8000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F7A6),
    DeviceInfo("F3", "STM32F378xx", 0x432, 0x50, ram=(0x_2000_1000, 0x_2000_8000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F), bootloader_id_address=0x_1FFF_F7A6),
    # FIXME different flash size for both devices with PID=0x422 ?
    DeviceInfo("F3", "STM32F302xB(C)/303xB(C)", 0x422, 0x41, ram=(0x_2000_1400, 0x_2000_A000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F3", "STM32F358xx", 0x422, 0x50, ram=(0x_2000_1400, 0x_2000_A000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    # FIXME different flash size for both devices with PID=0x439 ?
    DeviceInfo("F3", "STM32F301xx/302x4(6/8)", 0x439, 0x40, ram=(0x_2000_1800, 0x_2000_4000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0801_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F3", "STM32F318xx", 0x439, 0x50, ram=(0x_2000_1800, 0x_2000_4000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0801_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F3", "STM32F303x4(6/8)/334xx/328xx", 0x438, 0x50, ram=(0x_2000_1800, 0x_2000_3000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0801_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    # FIXME different flash size for both devices with PID=0x446 ?
    DeviceInfo("F3", "STM32F302xD(E)/303xD(E)", 0x446, 0x40, ram=(0x_2000_1800, 0x_2001_0000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),
    DeviceInfo("F3", "STM32F398xx", 0x446, 0x50, ram=(0x_2000_1800, 0x_2001_0000), system=(0x_1FFF_D800, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB, 2), option=(0x_1FFF_F800, 0x_1FFF_F80F)),

    # FIXME different flash size for both devices with PID=0x413 ?
    DeviceInfo("F4", "STM32F40xxx/41xxx", 0x413, 0x31, ram=(0x_2000_2000, 0x_2002_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0810_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F), bootloader_id_address=0x_1FFF_77DE),
    DeviceInfo("F4", "STM32F40xxx/41xxx", 0x413, 0x91, ram=(0x_2000_3000, 0x_2002_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0810_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F), bootloader_id_address=0x_1FFF_77DE),
    # FIXME different flash size for both devices with PID=0x419 ?
    DeviceInfo("F4", "STM32F42xxx/43xxx", 0x419, 0x70, ram=(0x_2000_3000, 0x_2003_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0820_0000, Flash.F4_DUAL_BANK_PAGE_SIZE), option=(0x_1FFE_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F42xxx/43xxx", 0x419, 0x91, ram=(0x_2000_3000, 0x_2003_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0820_0000, Flash.F4_DUAL_BANK_PAGE_SIZE), option=(0x_1FFE_C000, 0x_1FFF_C00F)),
    # FIXME Check RAM upper end.
    DeviceInfo("F4", "STM32F401xB(C)", 0x423, 0xD1, ram=(0x_2000_3000, 0x_2001_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0804_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F401xD(E)", 0x433, 0xD1, ram=(0x_2000_3000, 0x_2001_8000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0808_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F410xx", 0x458, 0xB1, ram=(0x_2000_3000, 0x_2000_8000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0802_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F411xx", 0x431, 0xD0, ram=(0x_2000_3000, 0x_2002_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0808_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F412xx", 0x441, 0x90, ram=(0x_2000_3000, 0x_2004_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0810_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F446xx", 0x421, 0x90, ram=(0x_2000_3000, 0x_2002_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0808_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F469xx/479xx", 0x434, 0x90, ram=(0x_2000_3000, 0x_2006_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0820_0000, Flash.F4_DUAL_BANK_PAGE_SIZE), option=(0x_1FFE_C000, 0x_1FFF_C00F)),
    DeviceInfo("F4", "STM32F413xx/423xx", 0x463, 0x90, ram=(0x_2000_3000, 0x_2005_0000), system=(0x_1FFF_0000, 0x_1FFF_7800), flash=(0x_0800_0000, 0x_0818_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_C000, 0x_1FFF_C00F)),
    DeviceInfo("F7", "STM32F72xxx/73xxx", 0x452, 0x90, ram=(0x_2000_4000, 0x_2004_0000), system=(0x_1FF0_0000, 0x_1FF0_EDC0), flash=(0x_0800_0000, 0x_0808_0000, Flash.F2_F4_PAGE_SIZE), option=(0x_1FFF_0000, 0x_1FFF_001F)),
    # FIXME different flash size for both devices with PID=0x449 ?
    DeviceInfo("F7", "STM32F74xxx/75xxx", 0x449, 0x70, ram=(0x_2000_4000, 0x_2005_0000), system=(0x_1FF0_0000, 0x_1FF0_EDC0), flash=(0x_0800_0000, 0x_0810_0000, Flash.F7_PAGE_SIZE), option=(0x_1FFF_0000, 0x_1FFF_001F)),
    DeviceInfo("F7", "STM32F74xxx/75xxx", 0x449, 0x90, ram=(0x_2000_4000, 0x_2005_0000), system=(0x_1FF0_0000, 0x_1FF0_EDC0), flash=(0x_0800_0000, 0x_0810_0000, Flash.F7_PAGE_SIZE), option=(0x_1FFF_0000, 0x_1FFF_001F)),
    DeviceInfo("F7", "STM32F76xxx/77xxx", 0x451, 0x93, ram=(0x_2000_4000, 0x_2008_0000), system=(0x_1FF0_0000, 0x_1FF0_EDC0), flash=(0x_0800_0000, 0x_0820_0000, Flash.F7_PAGE_SIZE), option=(0x_1FFF_0000, 0x_1FFF_001F)),
    DeviceInfo("G0", "STM32G03xxx/04xxx", 0x466, 0x53, ram=(0x_2000_1000, 0x_2000_2000), system=(0x_1FFF_0000, 0x_1FFF_2000), flash=(0x_0800_0000, 0x_0801_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_787F), bootloader_id_address=0x_1FFF_1FFE),
    DeviceInfo("G0", "STM32G07xxx/08xxx", 0x460, 0xB3, ram=(0x_2000_2700, 0x_2000_9000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0802_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_787F), bootloader_id_address=0x_1FFF_6FFE),
    # FIXME different flash size for both devices with PID=0x467 ?
    # FIXME dual banks for system
    DeviceInfo("G0", "STM32G0B0xx", 0x467, 0xD0, ram=(0x_2000_4000, 0x_2002_0000), system=((0x_1FFF_0000, 0x_1FFF_7000), (0x_1FFF_8000, 0x_1FFF_F000)), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_787F), bootloader_id_address=0x_1FFF_9FFE),
    # FIXME dual banks for system
    DeviceInfo("G0", "STM32G0B1xx/0C1xx", 0x467, 0x92, ram=(0x_2000_4000, 0x_2002_0000), system=((0x_1FFF_0000, 0x_1FFF_6000), (0x_1FFF_8000, 0x_1FFF_F000)), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_787F), bootloader_id_address=0x_1FFF_9FFE),
    # FIXME: STM32flash has 0x_2000_4800 as upper system range.
    DeviceInfo("G0", "STM32G05xxx/061xx", 0x456, 0x51, ram=(0x_2000_1000, 0x_2000_2000), system=(0x_1FFF_0000, 0x_1FFF_1000), flash=(0x_0800_0000, 0x_0801_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_787F), bootloader_id_address=0x_1FFF_1FFE),
    DeviceInfo("G4", "STM32G431xx/441xx", 0x468, 0xD4, ram=(0x_2000_4000, 0x_2000_5800), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0802_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_782F)),
    DeviceInfo("G4", "STM32G47xxx/48xxx", 0x469, 0xD5, ram=(0x_2000_4000, 0x_2001_8000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_782F)),
    DeviceInfo("G4", "STM32G491xx/A1xx", 0x479, 0xD2, ram=(0x_2000_4000, 0x_2001_C000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_782F)),
    # FIXME Flash and option bytes?
    DeviceInfo("H5", "STM32H503xx", 0x474, 0xE1, ram=(0x_2000_4000, 0x_2000_8000), system=(0x_0BF8_7000, 0x_0BF9_0000), bootloader_id_address=0x_0BF8_FFFE),
    # FIXME Flash and option bytes?
    DeviceInfo("H5", "STM32H563xx/573xx", 0x484, 0xE3, ram=(0x_2000_0000, 0x_200A_0000), system=(0x_0BF9_7000, 0x_0BFA_0000), bootloader_id_address=0x_0BF9_FAFE),
    DeviceInfo("H7", "STM32H72xxx/73xxx", 0x483, 0x93, ram=((0x_2000_4100, 0x_2002_0000), (0x_2400_4000, 0x_2405_0000)), system=(0x_1FF0_0000, 0x_1FF1_E800), flash=(0x_0800_0000, 0x_0810_0000, 128 * kB), option=None, bootloader_id_address=0x_1FF1_E7FE),
    DeviceInfo("H7", "STM32H74xxx/75xxx", 0x450, 0x91, ram=((0x_2000_4100, 0x_2002_0000), (0x_2400_5000, 0x_2408_0000)), system=(0x_1FF0_0000, 0x_1FF1_E800), flash=(0x_0800_0000, 0x_0820_0000, 128 * kB), option=None, bootloader_id_address=0x_1FF1_E7FE),
    DeviceInfo("H7", "STM32H7A3xx/B3xx", 0x480, 0x92, ram=((0x_2000_4100, 0x_2002_0000), (0x_2403_4000, 0x_2408_0000)), system=(0x_1FF0_0000, 0x_1FF1_4000), flash=(0x_0800_0000, 0x_0810_0000, 8 * kB), option=None, bootloader_id_address=0x_1FF1_3FFE),

    DeviceInfo("L0", "STM32L01xxx/02xxx", 0x457, 0xC3, ram=None, system=(0x_1FF0_0000, 0x_1FF0_1000), flash=(0x_0800_0000, 0x_0800_4000, 128, 32), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_0FFE),
    DeviceInfo("L0", "STM32L031xx/041xx", 0x425, 0xC0, ram=(0x_2000_1000, 0x_2000_2000), system=(0x_1FF0_0000, 0x_1FF0_1000), flash=(0x_0800_0000, 0x_0800_8000, 128, 32), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_0FFE),
    DeviceInfo("L0", "STM32L05xxx/06xxx", 0x417, 0xC0, ram=(0x_2000_1000, 0x_2000_2000), system=(0x_1FF0_0000, 0x_1FF0_1000), flash=(0x_0800_0000, 0x_0801_0000, 128, 32), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_0FFE),
    # FIXME different flash size for both devices with PID=0x447 ?
    # Note: STM32flash has 0x_2000_2000 as lower system range.
    DeviceInfo("L0", "STM32L07xxx/08xxx", 0x447, 0x41, ram=(0x_2000_1000, 0x_2000_5000), system=(0x_1FF0_0000, 0x_1FF0_2000), flash=(0x_0800_0000, 0x_0803_0000, 128, 32), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_1FFE),
    DeviceInfo("L0", "STM32L07xxx/08xxx", 0x447, 0xB2, ram=(0x_2000_1400, 0x_2000_5000), system=(0x_1FF0_0000, 0x_1FF0_2000), flash=(0x_0800_0000, 0x_0803_0000, 128, 32), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_1FFE),

    DeviceInfo("L1", "STM32L1xxx6(8/B)", line="Medium-density ULP", pid=0x416, bid=0x20, ram=(0x_2000_0800, 0x_2000_4000), system=(0x_1FF0_0000, 0x_1FF0_2000), flash=(0x_0800_0000, 0x_0802_0000, 256, 16), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_0FFE),
    DeviceInfo("L1", "STM32L1xxx6(8/B)A", 0x429, 0x20, ram=(0x_2000_1000, 0x_2000_8000), system=(0x_1FF0_0000, 0x_1FF0_2000), flash=(0x_0800_0000, 0x_0802_0000, 256, 16), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_0FFE),
    DeviceInfo("L1", "STM32L1xxxC", 0x427, 0x40, ram=(0x_2000_1000, 0x_2000_8000), system=(0x_1FF0_0000, 0x_1FF0_2000), flash=(0x_0800_0000, 0x_0804_0000, 256, 16), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_1FFE),
    DeviceInfo("L1", "STM32L1xxxD", 0x436, 0x45, ram=(0x_2000_1000, 0x_2000_C000), system=(0x_1FF0_0000, 0x_1FF0_2000), flash=(0x_0800_0000, 0x_0806_0000, 256, 16), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_1FFE),
    DeviceInfo("L1", "STM32L1xxxE", 0x437, 0x40, ram=(0x_2000_1000, 0x_2001_4000), system=(0x_1FF0_0000, 0x_1FF0_2000), flash=(0x_0800_0000, 0x_0808_0000, 256, 16), option=(0x_1FF8_0000, 0x_1FF8_001F), bootloader_id_address=0x_1FF0_1FFE),
    # Note: Stm32flash has 0x_2000_3100 as ram start.
    DeviceInfo("L4", "STM32L412xx/422xx", line="Low-density", pid=0x464, bid=0xD1, ram=(0x_2000_2100, 0x_2000_8000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0802_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_780F)),
    DeviceInfo("L4", "STM32L43xxx/44xxx", 0x435, 0x91, ram=(0x_2000_3100, 0x_2000_C000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_780F)),
    DeviceInfo("L4", "STM32L45xxx/46xxx", 0x462, 0x92, ram=(0x_2000_3100, 0x_2002_0000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_780F), flags=DeviceFlag.CLEAR_PEMPTY),
    # FIXME different flash size for both devices with PID=0x415 ?
    DeviceInfo("L4", "STM32L47xxx/48xxx", 0x415, 0xA3, ram=(0x_2000_3000, 0x_2001_8000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0810_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_F80F)),
    DeviceInfo("L4", "STM32L47xxx/48xxx", 0x415, 0x92, ram=(0x_2000_3100, 0x_2001_8000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0810_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_F80F)),
    DeviceInfo("L4", "STM32L496xx/4A6xx", 0x461, 0x93, ram=(0x_2000_3100, 0x_2004_0000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0810_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_F80F)),
    DeviceInfo("L4", "STM32L4Rxx/4Sxx", 0x470, 0x95, ram=(0x_2000_3200, 0x_200A_0000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0810_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_F80F)),
    DeviceInfo("L4", "STM32L4P5xx/Q5xx", 0x471, 0x90, ram=(0x_2000_4000, 0x_2005_0000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0810_0000, 4 * kB), option=(0x_1FF0_0000, 0x_1FF0_000F)),
    DeviceInfo("L5", "STM32L552xx/562xx", 0x472, 0x92, ram=(0x_2000_4000, 0x_2004_0000), system=(0x_0BF9_0000, 0x_0BF9_8000), flash=(0x_0800_0000, 0x_0808_0000, 2 * kB), option=None, bootloader_id_address=0x_0BF9_7FFE),
    # FIXME flash config ?
    DeviceInfo("WBA", "STM32WBA52xx", 0x492, 0xB0, ram=(0x_2000_0000, 0x_2000_2000), system=(0x_0BF8_8000, 0x_0BF9_0000), bootloader_id_address=0x_0BF8_FEFE),
    DeviceInfo("WB", "STM32WB10xx/15xx", 0x494, 0xB1, ram=(0x_2000_5000, 0x_2004_0000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0805_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_787F), bootloader_id_address=0x_1FFF_6FFE),
    DeviceInfo("WB", "STM32WB30xx/35xx/50xx/55xx", 0x495, 0xD5, ram=(0x_2000_4000, 0x_2000_C000), system=(0x_1FFF_0000, 0x_1FFF_7000), flash=(0x_0800_0000, 0x_0810_0000, 4 * kB), option=(0x_1FFF_8000, 0x_1FFF_807F), bootloader_id_address=0x_1FFF_6FFE),
    DeviceInfo("WL", "STM32WLE5xx/WL55xx", 0x497, 0xC4, ram=(0x_2000_2000, 0x_2001_0000), system=(0x_1FFF_0000, 0x_1FFF_4000), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB), option=(0x_1FFF_7800, 0x_1FFF_8000), bootloader_id_address=0x_1FFF_3EFE),
    # FIXME flash config?
    DeviceInfo("U5", "STM32U535xx/545xx", 0x455, 0x91, ram=(0x_2000_4000, 0x_2024_0000), system=(0x_0BF9_0000, 0x_0BFA_0000), bootloader_id_address=0x_0BF9_9EFE),
    #
    DeviceInfo("U5", "STM32U575xx/585xx", 0x482, 0x92, ram=(0x_2000_4000, 0x_200C_0000), system=(0x_0BF9_0000, 0x_0BFA_0000), flash=(0x_0800_0000, 0x_0820_0000, 8 * kB), option=None, bootloader_id_address=0x_0BF9_9EFE),
    # FIXME flash config?
    DeviceInfo("U5", "STM32U595xx/599xx/5A9xx", 0x481, 0x92, ram=(0x_2000_4000, 0x_2027_0000), system=(0x_0BF9_0000, 0x_0BFA_0000), bootloader_id_address=0x_0BF9_9EFE),

    # Not yet in AN2606.  Bootloader IDs are unknown.
    # Assumption: 'Medium-density performance' refers to F1 series, and F103.
    # FIXME No bootloader ID address?
    DeviceInfo("F1", "STM32F103x8/B", line="Medium-density performance", pid=0x641, bid=None, ram=(0x_2000_0200, 0x_2000_5000), system=(0x_1FFF_F000, 0x_1FFF_F800), flash=(0x_0800_0000, 0x_0802_0000, 1 * kB, 4), option=(0x_1FFF_F800, 0x_1FFF_F80F)),

    # WBA, WB, WL or simply 'W'?
    # FIXME bootloader ID address?
    DeviceInfo("W", "STM32W", variant="128kB", pid=0x9A8, bid=None, ram=(0x_2000_0200, 0x_2000_2000), system=(0x_0804_0000, 0x_0804_0800), flash=(0x_0800_0000, 0x_0802_0000, 1 * kB, 4), option=(0x_0804_0800, 0x_0804_080F)),
    DeviceInfo("W", "STM32W", variant="256kB", pid=0x9B0, bid=None, ram=(0x_2000_0200, 0x_2000_4000), system=(0x_0804_0000, 0x_0804_0800), flash=(0x_0800_0000, 0x_0804_0000, 2 * kB, 4), option=(0x_0804_0800, 0x_0804_080F)),

    # ST BlueNRG
    DeviceInfo("NRG", "BlueNRG-1", pid=0x03, bid=None, ram=(0x_2000_0000, 0x_2000_6000), system=(0x_1000_0000, 0x_1000_0800), flash=(0x_1004_0000, 0x_1006_8000, 2 * kB)),
    DeviceInfo("NRG", "BlueNRG-2", pid=0x2F, bid=None, ram=(0x_2000_0000, 0x_2000_6000), system=(0x_1000_0000, 0x_1000_0800), flash=(0x_1004_0000, 0x_1008_0000, 2 * kB)),
    # There is a 32kB RAM variant of BlueNRG-LP, but that can't be determined from bootloader
    DeviceInfo("NRG", "BlueNRG-LP", pid=0x3F, bid=None, ram=(0x_2000_0000, 0x_2001_0000), system=(0x_1000_0000, 0x_1000_1800), flash=(0x_1004_0000, 0x_1008_0000, 2 * kB)),
    DeviceInfo("NRG", "BlueNRG-LPS", pid=0x3B, bid=None, ram=(0x_2000_0000, 0x_2000_6000), system=(0x_1000_0000, 0x_1000_1800), flash=(0x_1004_0000, 0x_1007_0000, 2 * kB)),

    # Wiznet W7500
    DeviceInfo("WIZ", "Wiznet W7500", 0x801, bid=None, ram=None, system=None),
]

DEVICES = {(dev.product_id, dev.bootloader_id): dev for dev in DEVICE_DETAILS}

# If devices are not yet registered with bootloader_id == None, then do so.
for device in DEVICE_DETAILS:
    if (device.product_id, None) in DEVICES:
        continue
    DEVICES[(device.product_id, None)] = device
