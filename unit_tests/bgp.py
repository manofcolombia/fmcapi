import logging
import fmcapi


def test__bgp(fmc):
    logging.info("Test Device BGP.")

    bgp_device = fmcapi.BGP(fmc=fmc)
    bgp_device.device_name = 'FTDV'
    bgp_device.asNumber = 65333
    bgp_device.addressFamilyIPv4 = {}
    bgp_device.addressFamilyIPv4['neighbors'] = [
        {
            'remoteAs' : '65334',
            'ipv4Address' : '2.2.2.2',
            'type' : 'neighboripv4'
        }
    ]
    bgp_device.post()

    bgp_device.get()

    if 'addressFamilyIPv4' in bgp_device.__dict__:
        logging.info(f'BGP IPv4 Address Family in use')
        if 'neighbors' in bgp_device.addressFamilyIPv4:
            if len(bgp_device.addressFamilyIPv4['neighbors']) > 0:
                logging.info(f'BGP IPv4 Neighbors found. Proceeding to admin shutdown...')
                for neighbor in bgp_device.addressFamilyIPv4['neighbors']:
                    neighbor['neighborGeneral']['shutdown'] = True
                    logging.info(f"Neighbor: {neighbor['ipv4Address']}, state: {neighbor['neighborGeneral']['shutdown']}")
                bgp_device.put()
    bgp_device.get()
    bgp_device.delete()

    logging.info("Test Device BGP done.\n")