#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

CLI_CMD = {
    # Connection and memory manipulation commands
    'List': '-List',
    # Description: Lists the corresponding firmware version and the unique Serial Number (SN)
    # of every ST-LINK probe connected to the computer.
    # Note: To have a correct SN, the ST-LINK firmware version must be:
    # • V1J13S0 or greater for ST-LINK.
    # • V2J21S4 or greater for ST-LINK/V2.
    # • V2J21M5 or greater for ST-LINK/V2-1.
    # When an ST-LINK/v2 or ST-LINK/V2-1 probe is used with another application, the serial
    # number is not displayed and the probe cannot be used in the current instance of the
    # ST-LINK utility.
    'r8': '-r8',
    # Description: Reads <NumBytes> memory.
    # Syntax: -r8 <Address> <NumBytes>
    # Example: -r8 0x20000000 0x100
    'w8': '-w8',
    # Description: Writes 8-bit data to the specified memory address.
    # Syntax: -w8 <Address> <data>
    # Example: -w8 0x20000000 0xAA
    # Note: -w8 supports writing to Flash memory, OTP, SRAM and R/W registers.
    'w32': '-w32',
    # Description: Writes 32-bit data to the specified memory address.
    # Syntax: -w32 <Address> <data>
    # Example: -w32 0x08000000 0xAABBCCDD
    # Note: -w32 supports writing to Flash memory, OTP, SRAM and R/W registers.

    # Core commands
    'Rst': '-Rst',
    # Description: Resets the system.
    # Syntax: -Rst
    'HardRst': '-HardRst',
    # Description: Hardware reset.
    # Syntax: -HardRst
    # Note: -HardRst command is available only with ST-LINK/V2. The RESET pin of the JTAG
    # connector (pin 15) must be connected to the device reset pin.
    'Run': '-Run',
    # Description: Sets the program counter and stack pointer as defined at user application and
    # performs a run operation.
    # Syntax:-Run [<Address>]
    # Example: -run 0x08003000
    'Halt': '-Halt',
    # Description: Halts the core.
    # Syntax: -Halt
    'Step': '-Step',
    # Description: Executes Step core instruction.
    # Syntax:-Step
    'SetBP': '-SetBP',
    # Description: Sets the software or hardware breakpoint at a specific address. If an
    # address is not specified, 0x08000000 is used.
    # Syntax: -SetBP [<Address>]
    # Example: -SetBP 0x08003000
    'ClrBP': '-ClrBP',
    # Description: Clears all hardware breakpoints, if any.
    # Syntax: -ClrBP
    'CoreReg': '-CoreReg',
    # Description: Reads the Core registers.
    # Syntax: -CoreReg
    'SCore': '-SCore',
    # Description: Detects the Core status.
    # Syntax: -SCore

    # Flash commands
    'ME': '-ME',
    # Description: Executes a Full chip erase operation.
    # Syntax: -ME
    'SE': '-SE',
    # Description: Erases Flash sector(s).
    # Syntax: -SE <Start_Sector> [<End_Sector>]
    # Example: -SE 0 => Erase sector 0
    # -SE 2 12 => Erase sectors from 2 to 12
    # *For STM32L Series, the following cmd erases data eeprom:
    # -SE ed1 => Erases data eeprom at 0x08080000
    # -SE ed2 => Erases data eeprom at 0x08081800
    'P': '-P',
    # Description: Loads binary, Intel Hex or Motorola S-record file into device memory without
    # verification. For hex and srec format, the address is relevant.
    # Syntax: -P <File_Path> [<Address>]
    # Examples: -P C:\file.srec
    # -P C:\file.bin 0x08002000
    # -P C:\file.hex
    # Note: Depending on the STM32 supply voltage, STM32F2 and STM32F4 Series support different
    # programming modes . When using ST-LINK/V2 or ST-LINK-V3, the supply voltage is
    # detected automatically. Therefore, the correct programming mode is selected. When using
    # ST-LINK, the 32-bit programming mode is selected by default.
    # If the device is read-protected, the protection is disabled. If some Flash memory pages are
    # write-protected, the protection is disabled during programming and then recovered.
    'V': '-V',
    # Description: Verifies that the programming operation was performed successfully.
    # Syntax: -V [while_programming/after_programming]
    # Example: -P *C:\file.srec* -V "after_programming"
    # Note: If no argument is provided the while_programming verification method is performed.

    # Miscellaneous commands
    'CmpFile': '-CmpFile',
    # Description: Compares a binary, Intel Hex or Motorola S-record file with device memory
    # and displays the address of the first different value.
    # Syntax: -CmpFile <File_Path> [<Address>]
    # Example1: -CmpFile "c:\\application.bin" 0x08000000
    # Example2: -CmpFile "c:\\application.hex
    # The user can also compare the file content with an external memory. The path of the
    # external memory loader must be specified by the -EL cmd.
    # Example1: -CmpFile "c:\application.bin" 0x64000000 -EL "c:\Custom-Flash-Loader.stldr"
    'Cksum': '-Cksum',
    # Description: Calculates the Checksum value of a given file or a specified memory zone.
    # The algorithm used is the simple arithmetic sum algorithm, byte per byte. The result is
    # truncated to 32-bit word.
    # Syntax: -Cksum <File_Path>
    # -Cksum <Address> <Size>
    # Example1: -Cksum "C:\File.hex"
    # Example2: -Cksum 0x08000000 0x200
    # Example3: -Cksum 0x90000000 0x200 -EL "C:\Custom_Flash_Loader.stldr"
    'Dump': '-Dump',
    # Description: Reads target memory and save it in a file
    # Syntax: -Dump<Address> <Memory_Size> <File_Path>
    'Log': '-Log',
    # Description: Enables Trace LOG file generation.
    # The log file is generated under %userprofile%\STMicroelectronics\ST-LINK utility.
    'NoPrompt': '-NoPrompt',
    # Description: Disables user confirmation prompts (For example, to program RDP Level 2 within a file).
    'Q': '-Q',
    # Description: Enables quiet mode. No progress bar displayed.
    'TVolt': '-TVolt',
    # Description: Enables quiet

    # Option bytes commands
    'rOB': '-rOB',
    # Description: Displays all option bytes.
    # Syntax: -rOB
    'OB': '-OB',
    # Description: Configures the option bytes. This command:
    # • sets the Read Protection Level to Level 0 (no protection)
    # • sets the IWDG_SW option to ‘1’ (watchdog enabled by software)
    # • sets the nRST_STOP option to ‘0’ (reset generated when entering Standby mode)
    # • sets the Data0 option byte
    # • sets the Data1 option byte
    # Syntax: -OB [RDP=<Level>][BOR_LEV=<Level>][IWDG_SW=<Value>]
    # [nRST_STOP=<Value>][nRST_STDBY=<Value>][nBFB2=<Value>]
    # [nBoot1=<Value>][nSRAM_Parity=<Value>][Data0=<Value>]
    # [SPRMOD=<Value>][Data1=<Value>][WRP=<Value>][WRP2=<Value>]
    # [WRP3=<Value>][WRP4=<Value>]
    # [BOOT_ADD0=<Value>]
    # [BOOT_ADD1=<Value>]
    # Example:–OB RDP=0 IWDG_SW=1 nRST_STOP=0 Data0=0xAA Data1=0xBC
    # Option byte command parameter descriptions see page 41

    # External memory command25
    'EL': '-EL',
    # Description: Selects a custom Flash memory loader for external memory operations.
    # Syntax: -EL [<loader_File_Path>]
    # Example: -P c:\\application.hex -EL c:\\Custom-Flash-Loader.stldr
}


class StLink(object):
    def __init__(self):
        self.path = 'ST-LINK_CLI.exe'
        self.err = {
            1: 'STM32 ST-LINK Command Line Interface',
            -1: 'No ST-LINK detected',
            -255: 'unknown error'
        }
        self.cmd = CLI_CMD

    def run(self, cmd):
        data = ''
        tx = '{} {}'.format(self.path, cmd)
        proc = Popen(tx, stdout=PIPE, shell=True)
        for dat in iter(proc.stdout.readline, b''):
            dat = dat.decode('utf-8', 'ignore').strip()
            if dat == '':
                continue
            print('CMD rx:' + dat)
            data += dat + '\n'
        proc.stdout.close()
        proc.wait()
        return str(data)

    def check_err(self, data):
        if self.err[1] in data:
            if self.err[-1] in data:
                print(self.err[-1])
                return False
            return True
        else:
            print(self.err[-255])
            return False

    def set_reset(self):
        cmd = self.cmd['Rst']
        self.run(cmd)

    def read_info(self):
        cmd = self.cmd['rOB']
        rep = self.run(cmd)
        if self.check_err(rep):
            if 'Device ID' in rep:
                _device_id = rep[rep.rfind('Device ID'):].split('\n')[0]
                print(_device_id)
            if 'Device flash' in rep:
                _device_flash = rep[rep.rfind('Device flash'):].split('\n')[0]
                print(_device_flash)
            if 'Device family' in rep:
                _device_family = rep[rep.rfind('Device family'):].split('\n')[0]
                print(_device_family)

    def read_protect(self):
        cmd = self.cmd['rOB']
        rep = self.run(cmd)
        if self.check_err(rep) and 'RDP' in rep:
            _rdp_line = rep[rep.rfind('RDP'):].split('\n')[0].strip()
            _level = _rdp_line.split(':')[1].strip()
            return _level

    def write_protect(self):
        cmd = '{} RDP=1'.format(self.cmd['OB'])
        rep = self.run(cmd)
        if self.check_err(rep):
            return True
        return False

    def write_disprotect(self):
        cmd = '{} RDP=0'.format(self.cmd['OB'])
        rep = self.run(cmd)
        if self.check_err(rep):
            return True
        return False

    def program_file(self, file, verify=False, mode=0):
        mode_dict = {0: 'while_programming', 1: 'after_programming'}
        ftype = file[file.rfind('.')+1:].upper()
        cmd = '-P %s' % file
        if ftype == 'BIN':
            cmd += ' 0x08000000'
        if verify:
            cmd += ' -V'
            if mode > 0:
                cmd += ' \"%s\"' % mode_dict[mode]
        rep = self.run(cmd)
        if self.check_err(rep):
            return True
        return False


if __name__ == '__main__':
    st = StLink()
    st.program_file('test.bin', verify=True)
    st.read_info()
    st.set_reset()
