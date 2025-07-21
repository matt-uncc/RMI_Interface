import struct


def hspo_extract(data, required_length, binary_format):
    if len(data) >= int(required_length):
        unpacked = struct.unpack(binary_format, data[:required_length])
        return unpacked[5], unpacked[6], unpacked[7], unpacked[8], unpacked[9], unpacked[10]
    return None
