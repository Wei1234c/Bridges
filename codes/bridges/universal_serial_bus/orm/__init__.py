import math
from array import array



class OrmClassBase:
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1))
    BYTEORDER = 'little'

    @classmethod
    def int_to_byte_array(cls, value, length = None, byteorder = BYTEORDER, signed = False):
        length = math.ceil(math.log2(value + 1) / 8) if length is None else length
        length = max(length, 1)
        return array('B', value.to_bytes(length, byteorder, signed = signed))


    @classmethod
    def int_to_hex(cls, value, length = None, byteorder = BYTEORDER, signed = False):
        byte_array = cls.int_to_byte_array(value, length, byteorder, signed)
        return cls.byte_array_to_hex(byte_array)


    @classmethod
    def byte_array_to_int(cls, byte_array, byteorder = BYTEORDER, signed = False):
        return int.from_bytes(byte_array.tobytes(), byteorder = byteorder, signed = signed)


    @classmethod
    def hex_to_int(cls, hex_string, byteorder = BYTEORDER, signed = False):
        return int.from_bytes(bytes.fromhex(hex_string), byteorder = byteorder, signed = signed)


    @classmethod
    def byte_array_to_hex(cls, byte_array):
        return byte_array.tobytes().hex()


    @classmethod
    def hex_to_byte_array(cls, hex_string):
        return array('B', bytes.fromhex(hex_string))


    @classmethod
    def get_descriptor_fields_values(cls, descriptor_array, to_hex = True):
        fields_values = []
        start = 0

        for i in range(len(cls.fields_sizes)):
            size = cls.fields_sizes[i][1]
            value = descriptor_array[start: start + size]
            fields_values.append(cls.byte_array_to_hex(value) if to_hex else value)
            start += size

        return fields_values


    @classmethod
    def split_descriptor(cls, descriptor):
        total_len = len(descriptor)
        start = 0

        while start < total_len:
            seg_len = descriptor[start]
            yield descriptor[start: start + seg_len]
            start = start + seg_len
