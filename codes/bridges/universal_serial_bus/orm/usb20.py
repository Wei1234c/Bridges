from bridges.universal_serial_bus.orm import OrmClassBase



class ClassCode:
    fields_sizes = (('code', 1),)


    def __init__(self, description, descriptor_usage, base_code):
        self.description = description
        self.descriptor_usage = descriptor_usage
        self.base_code = base_code



class DescriptorType(OrmClassBase):
    fields_sizes = (('bDescriptorType', 1),)


    def __init__(self, dscrpt_type, bDescriptorType):
        self.dscrpt_type = dscrpt_type
        self.bDescriptorType = bDescriptorType



class DscptDevice(OrmClassBase):
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1), ('bcdUSB', 2), ('bDeviceClass', 1), ('bDeviceSubClass', 1),
                    ('bDeviceProtocol', 1), ('bMaxPacketSize0', 1), ('idVendor', 2), ('idProduct', 2), ('bcdDevice', 2),
                    ('iManufacturer', 1), ('iProduct', 1), ('iSerialNumber', 1), ('bNumConfigurations', 1))


    def __init__(self, device_id, bLength, bDescriptorType, bcdUSB, bDeviceClass, bDeviceSubClass, bDeviceProtocol,
                 bMaxPacketSize0, idVendor, idProduct, bcdDevice, iManufacturer, iProduct, iSerialNumber,
                 bNumConfigurations):
        self.device_id = device_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bcdUSB = bcdUSB
        self.bDeviceClass = bDeviceClass
        self.bDeviceSubClass = bDeviceSubClass
        self.bDeviceProtocol = bDeviceProtocol
        self.bMaxPacketSize0 = bMaxPacketSize0
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.bcdDevice = bcdDevice
        self.iManufacturer = iManufacturer
        self.iProduct = iProduct
        self.iSerialNumber = iSerialNumber
        self.bNumConfigurations = bNumConfigurations



class DscptConfiguration(OrmClassBase):
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1), ('wTotalLength', 2), ('bNumInterfaces', 1),
                    ('bConfigurationValue', 1), ('iConfiguration', 1), ('bmAttributes', 1), ('bMaxPower', 1))


    def __init__(self, device_id, bLength, bDescriptorType, wTotalLength, bNumInterfaces, bConfigurationValue,
                 iConfiguration, bmAttributes, bMaxPower):
        self.device_id = device_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.wTotalLength = wTotalLength
        self.bNumInterfaces = bNumInterfaces
        self.bConfigurationValue = bConfigurationValue
        self.iConfiguration = iConfiguration
        self.bmAttributes = bmAttributes
        self.bMaxPower = bMaxPower



class DscptInterface(OrmClassBase):
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1), ('bInterfaceNumber', 1), ('bAlternateSetting', 1),
                    ('bNumEndpoints', 1), ('bInterfaceClass', 1), ('bInterfaceSubClass', 1), ('bInterfaceProtocol', 1),
                    ('iInterface', 1))


    def __init__(self, device_id, bConfigurationValue, bLength, bDescriptorType, bInterfaceNumber, bAlternateSetting,
                 bNumEndpoints, bInterfaceClass, bInterfaceSubClass, bInterfaceProtocol, iInterface):
        self.device_id = device_id
        self.bConfigurationValue = bConfigurationValue
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bInterfaceNumber = bInterfaceNumber
        self.bAlternateSetting = bAlternateSetting
        self.bNumEndpoints = bNumEndpoints
        self.bInterfaceClass = bInterfaceClass
        self.bInterfaceSubClass = bInterfaceSubClass
        self.bInterfaceProtocol = bInterfaceProtocol
        self.iInterface = iInterface



class DscptEndpoint(OrmClassBase):
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1), ('bEndpointAddress', 1), ('bmAttributes', 1),
                    ('wMaxPacketSize', 2), ('bInterval', 1))


    def __init__(self, device_id, bConfigurationValue, bInterfaceNumber, bAlternateSetting, bLength, bDescriptorType,
                 bEndpointAddress, bmAttributes, wMaxPacketSize, bInterval):
        self.device_id = device_id
        self.bConfigurationValue = bConfigurationValue
        self.bInterfaceNumber = bInterfaceNumber
        self.bAlternateSetting = bAlternateSetting
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bEndpointAddress = bEndpointAddress
        self.bmAttributes = bmAttributes
        self.wMaxPacketSize = wMaxPacketSize
        self.bInterval = bInterval



class DscptStringLangId(OrmClassBase):
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1), ('wLANGID', 2))


    def __init__(self, device_id, bLength, bDescriptorType, wLANGID):
        self.device_id = device_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.wLANGID = wLANGID



class DscptString(OrmClassBase):
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1))


    def __init__(self, device_id, str_id, string):
        self.device_id = device_id
        self.str_id = str_id
        self.string = string



class RequestCode(OrmClassBase):
    fields_sizes = (('rqst_code', 1),)


    def __init__(self, request_type, rqst_code):

        self.request_type = request_type
        self.rqst_code = rqst_code

class UsbDevice(OrmClassBase):
    fields_sizes = ()


    def __init__(self, name, description):
        self.name = name
        self.description = description
