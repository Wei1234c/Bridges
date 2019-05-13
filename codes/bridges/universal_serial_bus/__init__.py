import usb._interop
import usb._lookup

import bridges.universal_serial_bus._lookup
from bridges.universal_serial_bus.legacy import *



class USBdevice(usb.core.Device):
    TYPE = CONTROL_REQUEST.TYPE.STANDARD
    DEFAULT_INTERFACE = (0, 0)


    def __init__(self, vid, pid, address = None, configuration = None):
        kwargs = dict(idVendor = vid, idProduct = pid)
        if address is not None:
            kwargs['address'] = address
        dev = usb.core.find(**kwargs)
        if not dev:
            raise ValueError("Device not found ({:x}:{:x} address:{})".format(vid, pid, address or ''))

        super().__init__(dev._ctx.dev, dev._ctx.backend)
        self.set_configuration(configuration)
        self.set_interface(self.DEFAULT_INTERFACE)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def __del__(self):
        self.close()


    @property
    def is_open(self):
        return (self._ctx.handle is not None) if hasattr(self, '_ctx') else False


    def close(self):
        if self.is_open:
            usb.util.dispose_resources(self)
            self.reset()


    def set_interface(self, interface_idx):
        interface = self.get_active_configuration()[interface_idx]
        self.endpoints = {ep.bEndpointAddress: ep for ep in [Endpoint(ep) for ep in interface]}


    def control_read(self, bRequest, wValue = 0, wIndex = 0, wLength = 0x400, timeout = None, type = None,
                     recipient = CONTROL_REQUEST.RECIPIENT.DEVICE):
        type = self.TYPE if type is None else type
        bmRequestType = usb.util.build_request_type(CONTROL_REQUEST.DIRECTION.IN, type, recipient)
        return self.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength, timeout)


    def control_write(self, bRequest, wValue = 0, wIndex = 0, data = None, timeout = None, type = None,
                      recipient = CONTROL_REQUEST.RECIPIENT.DEVICE):
        type = self.TYPE if type is None else type
        bmRequestType = usb.util.build_request_type(CONTROL_REQUEST.DIRECTION.OUT, type, recipient)
        return self.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data, timeout)


    @classmethod
    def scan_usb_bus(cls, full = False):
        devices = list(usb.core.find(find_all = True))
        for dev in devices:
            print(dev if full else dev._str())
        return devices


    def get_descriptor(self, desc_size, desc_type, desc_index, wIndex = 0):
        return usb.control.get_descriptor(self, desc_size, desc_type, desc_index, wIndex)


    def get_string(self, index, langid = None):
        return usb.util.get_string(self, index, langid)


    def get_strings(self, lang_id = None, max = 127):
        descriptors = []

        for i in range(max):
            try:
                descriptors.append(self.get_string(i, lang_id))
            except usb.core.USBError:
                pass

        return descriptors



class Endpoint(usb.core.Endpoint):

    def __init__(self, endpoint):
        self.device = endpoint.device
        self.index = endpoint.index

        usb.core._set_attr(endpoint, self, (
            'bLength', 'bDescriptorType', 'bEndpointAddress', 'bmAttributes', 'wMaxPacketSize', 'bInterval', 'bRefresh',
            'bSynchAddress', 'extra_descriptors'))


    @property
    def direction(self):
        direction = usb.util.endpoint_direction(self.bEndpointAddress)
        return bridges.universal_serial_bus._lookup.endpoint_direction[direction]


    @property
    def type(self):
        return usb._lookup.ep_attributes[(self.bmAttributes & ENDPOINT.TYPE.MASK)]


    @property
    def type_direction(self):
        return self._str()



class Descriptor:
    pass
