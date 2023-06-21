import json


def read_json(idvalue, interface_name, data, table_values):
    # Find a list of all the device interface
    # configurations with the same interface
    for interface in data["frinx-uniconfig-topology:configuration"][
            "Cisco-IOS-XE-native:native"]["interface"][interface_name]:
        name = interface["name"]

        description = None
        if "description" in interface:
            description = interface["description"]

        max_frame_size = None
        if "mtu" in interface:
            max_frame_size = interface["mtu"]

        # Check if the interface is linked to any Port Channel
        port_channel_id = None
        if "Cisco-IOS-XE-ethernet:channel-group" in interface:
            channel_id_Name = interface["Cisco-IOS-XE-ethernet:channel-group"
                                        ]["number"]
            for y in table_values:
                if (f"Port-channel{channel_id_Name}") == y[2]:
                    port_channel_id = y[0]

        alldata = json.dumps(interface)
        table_values.append(
            (
                idvalue,
                None,
                f"{interface_name}{name}",
                description,
                alldata,
                None,
                None,
                port_channel_id,
                max_frame_size,
            )
        )
        idvalue += 1
    return idvalue


def read_values():
    table_values = []
    idvalue = 1
    config = open("configClear_v2.json")
    data = json.load(config)

    # Add all of the required data about device
    # interface configurations to table_values
    idvalue = read_json(idvalue, "Port-channel", data, table_values)
    idvalue = read_json(idvalue, "TenGigabitEthernet", data, table_values)
    idvalue = read_json(idvalue, "GigabitEthernet", data, table_values)
    # Here we could also in the future add BDI and
    # Loopback interfaces if we wished to
    # idvalue = read_json(idvalue, "BDI", data, table_values)
    # idvalue = read_json(idvalue, "Loopback", data, table_values)

    config.close()
    return table_values
