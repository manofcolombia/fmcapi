"""BGP General Settings Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .devicerecords import DeviceRecords
import logging


class BGP(APIClassTemplate):
    """The BGP Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "asNumber",
        "addressFamilyIPv4",

    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []

    PREFIX_URL = "/devices/devicerecords"
    URL_SUFFIX = "/routing/bgp"

    def __init__(self, fmc, **kwargs):
        """
        Initialize BGP object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for BGP class.")
        self.parse_kwargs(**kwargs)
        # The 'name' in the reponse always seems to be 'bgp' and without a matching name kwarg parsing the response doesn't happen
        self.name = "bgp"
        self.type = "bgp"

    def device(self, device_name):
        """
        Indentify device id if only device name is given for BGP management.

        :param device_name: (str) Name of device.
        :return: None
        """
        logging.debug("In device() for BGP class.")

        device1 = DeviceRecords(fmc=self.fmc)
        device1.name = device_name
        device1.get()
        if "id" in device1.__dict__:
            self.device_id = device1.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.device_id}{self.URL_SUFFIX}"
            self.device_added_to_url = True
        else:
            logging.warning(
                f'Device "{device_name}" not found.  Cannot manage bgp for device.'
            )

    def remove_max_paths(self):
        '''
        Handles Cisco not cleaning up their own api responses...
        [{'description': 'maximumPaths is deprecated, use ebgp and ibgp instead.'}], 'severity': 'ERROR'}}
        '''
        if 'addressFamilyIPv4' in self.__dict__:
            if 'maximumPaths' in self.addressFamilyIPv4:
                logging.info(f'Removing maximumPaths from addressFamilyIPv4. Cisco has deprecated this. Utilize ebgp/ibgp instead')
                del self.addressFamilyIPv4['maximumPaths']

    def get(self, **kwargs):
        if "device_id" not in self.__dict__:
            self.device(self.device_name)
        response = super().get(**kwargs)
        return response

    def post(self, **kwargs):
        if "device_id" not in self.__dict__:
            self.device(self.device_name)
        self.remove_max_paths()
        response = super().post(**kwargs)
        return response

    def put(self, **kwargs):
        if "device_id" not in self.__dict__:
            self.device(self.device_name)
        self.remove_max_paths()
        response = super().put(**kwargs)
        return response

    def delete(self, **kwargs):
        if "device_id" not in self.__dict__:
            self.device(self.device_name)
        response = super().delete(**kwargs)
        return response