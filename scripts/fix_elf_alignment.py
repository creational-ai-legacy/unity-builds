#!/usr/bin/env python3
"""
ELF 16KB Page Size Alignment Fix Script

This script fixes native libraries (.so files) to be compatible with 16KB page size
devices required for Google Play Store submissions starting November 1st, 2025.

Usage:
    python3 fix_elf_alignment.py <path_to_library.so>

The script modifies ELF headers to set LOAD segment alignment from 4KB to 16KB.
It supports both 32-bit (armeabi-v7a) and 64-bit (arm64-v8a) libraries.
"""

import struct
import sys
import shutil
import os

def fix_elf_alignment(lib_path):
    """
    Fix ELF file LOAD segment alignment to 16KB (0x4000)
    
    Args:
        lib_path (str): Path to the .so library file
    """
    if not os.path.exists(lib_path):
        print(f'Library file not found: {lib_path}')
        return False
    
    # Create backup
    backup_path = lib_path + '.backup'
    try:
        shutil.copy2(lib_path, backup_path)
        print(f'Created backup: {backup_path}')
    except Exception as e:
        print(f'Failed to create backup: {e}')
        return False
    
    try:
        with open(backup_path, 'rb') as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f'Failed to read library file: {e}')
        return False
    
    # Check if it's a valid ELF file
    if len(data) < 64 or data[:4] != b'\x7fELF':
        print(f'Not an ELF file: {lib_path}')
        return False
    
    # Determine ELF class (32-bit or 64-bit)
    is_64bit = data[4] == 2
    is_32bit = data[4] == 1
    
    if not (is_64bit or is_32bit):
        print(f'Unknown ELF class: {lib_path} (class={data[4]})')
        return False
    
    elf_type = "64-bit" if is_64bit else "32-bit"
    print(f'Processing {elf_type} ELF file: {os.path.basename(lib_path)}')
    
    # Find program header table
    try:
        if is_64bit:
            # 64-bit ELF format
            ph_offset = struct.unpack('<Q', data[32:40])[0]  # e_phoff
            ph_entsize = struct.unpack('<H', data[54:56])[0]  # e_phentsize
            ph_num = struct.unpack('<H', data[56:58])[0]      # e_phnum
        else:
            # 32-bit ELF format
            ph_offset = struct.unpack('<I', data[28:32])[0]  # e_phoff
            ph_entsize = struct.unpack('<H', data[42:44])[0]  # e_phentsize
            ph_num = struct.unpack('<H', data[44:46])[0]      # e_phnum
    except struct.error as e:
        print(f'Failed to parse ELF header: {e}')
        return False
    
    print(f'Program headers: {ph_num} entries at offset 0x{ph_offset:x}')
    
    # Iterate through program headers and fix LOAD segment alignment
    fixed_segments = 0
    for i in range(ph_num):
        ph_start = ph_offset + i * ph_entsize
        
        if ph_start + 8 > len(data):
            print(f'Warning: Program header {i} extends beyond file')
            continue
            
        try:
            p_type = struct.unpack('<I', data[ph_start:ph_start+4])[0]
        except struct.error:
            print(f'Warning: Could not read program header {i}')
            continue
        
        if p_type == 1:  # PT_LOAD
            try:
                if is_64bit:
                    # Set p_align to 16KB (0x4000) for 64-bit
                    align_offset = ph_start + 48
                    if align_offset + 8 <= len(data):
                        current_align = struct.unpack('<Q', data[align_offset:align_offset+8])[0]
                        data[align_offset:align_offset+8] = struct.pack('<Q', 0x4000)
                        fixed_segments += 1
                        print(f'  Fixed LOAD segment {i}: 0x{current_align:x} -> 0x4000')
                else:
                    # Set p_align to 16KB (0x4000) for 32-bit
                    align_offset = ph_start + 28
                    if align_offset + 4 <= len(data):
                        current_align = struct.unpack('<I', data[align_offset:align_offset+4])[0]
                        data[align_offset:align_offset+4] = struct.pack('<I', 0x4000)
                        fixed_segments += 1
                        print(f'  Fixed LOAD segment {i}: 0x{current_align:x} -> 0x4000')
            except struct.error as e:
                print(f'Warning: Could not fix LOAD segment {i}: {e}')
    
    if fixed_segments == 0:
        print(f'No LOAD segments found to fix in {lib_path}')
        return False
    
    # Write fixed file
    try:
        with open(lib_path, 'wb') as f:
            f.write(data)
        print(f'Successfully fixed {fixed_segments} LOAD segments in {lib_path}')
        return True
    except Exception as e:
        print(f'Failed to write fixed library: {e}')
        # Restore backup on failure
        try:
            shutil.copy2(backup_path, lib_path)
            print(f'Restored backup due to write failure')
        except:
            pass
        return False

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python3 fix_elf_alignment.py <path_to_library.so>")
        print("\nThis script fixes ELF LOAD segment alignment from 4KB to 16KB")
        print("for compatibility with Android 15+ 16KB page size devices.")
        sys.exit(1)
    
    lib_path = sys.argv[1]
    
    print(f"Fixing 16KB alignment for: {lib_path}")
    success = fix_elf_alignment(lib_path)
    
    if success:
        print("✅ ELF alignment fix completed successfully")
        sys.exit(0)
    else:
        print("❌ ELF alignment fix failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
