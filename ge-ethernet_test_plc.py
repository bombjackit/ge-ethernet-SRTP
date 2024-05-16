from lib.GE_SRTP import *
import time
import json
import builtins

# Line 1 PLC IP address
# plc_ip = '4.120.143.1'
# Line 2 PLC IP address
# plc_ip = '4.120.142.1'
# Andon PLC IP address
# plc_ip = '4.120.200.1'
# Quality PLC IP address
# plc_ip = '4.120.80.10'
plc_ip = '4.120.28.18'

plc_list = [
    '4.101.108.251',
    '4.120.28.15',
    '4.120.28.17',
    '4.120.28.18',
    '4.120.60.47',
    '4.120.80.1',
    '4.120.80.10',
    '4.120.90.100',
    '4.120.90.101',
    '4.120.90.102',
    '4.120.90.103',
    '4.120.90.106',
    '4.120.90.107',
    '4.120.90.108',
    '4.120.90.109',
    '4.120.90.110',
    '4.120.90.111'
]

# PLC tags
plc_tags = {
    # "encoder": "R7354",
    # "line speed": "R5032",
    # "moving": "Q00065",
    # "andon1": "MB03521",
    # "andon2": "MB03522",
    # "andon3": "MB03523",
    "T1 Body": "R20000:2",
    "T1 Seq": "R20002:2",
    "T2 Body": "R20004:2",
    "T2 Seq": "R20006:2",
}

# Buffer print function that logs to a file
def print_and_log(content):
    with open("nissan-ge--10-00--14-may.log", "a") as file:
        print(content, file=file, flush=True)
    print(content)

# Function to connect to the PLC
def connect_to_plc(ip):
    plc = GeSrtp(ip)
    plc.initConnection()
    return plc

def parse_tag_data(data, data_type):
    parsed_data = ''
    if data_type == 'int array':
        for d in data:
            parsed_data += chr(d)
    elif data_type == 'byte_string':
        decoded_string = data.decode("utf-8", "ignore")
        parsed_data = ''.join(char for char in decoded_string if char.isprintable())
    else:
        parsed_data = data
    return parsed_data

# Function to read tags from the PLC
def read_tags(plc, tags, debug_logging=False):
    values = {}
    for tag_name, tag_address in tags.items():
        if debug_logging:
            print(f'READING: {tag_address}')
        try:
            res = plc.readSysMemory(tag_address, debug_logging)
        except Exception as e:
            print(f'Failed to read {tag_address}: {e}')
            continue
        if debug_logging:
            print(f'RES: {res.register_result}')
        values[tag_name] = res.register_result
        # if isinstance(values[tag_name], bytes):
        #     values[tag_name] = parse_tag_data(values[tag_name], 'byte_string')
    return values

# Main script
def main():
    debug_logging = False
    check_ip_list = False

    if check_ip_list:
        for p_ip in plc_list:
            plc = connect_to_plc(p_ip)
            try:
                current_values = read_tags(plc, plc_tags, debug_logging)
                print(f'Successfully read value {current_values} from plc ip {plc_ip}')
            except Exception as e:
                print(f'Failed to read from plc ip {plc_ip} with Error: {e}')
        return

    plc = connect_to_plc(plc_ip)
    last_values = {}

    while True:
        try:
            current_values = read_tags(plc, plc_tags)
            curr_ts = int(time.time()*1e3)
            for tag, value in current_values.items():
                if tag not in last_values or last_values[tag] != value:
                    print_and_log(f"{tag} tag '{plc_tags[tag]}' changed to {value} at: {curr_ts}")
            last_values = current_values
            time.sleep(1)
        except KeyboardInterrupt:
            print_and_log("Exiting...")
            break
        except Exception as e:
            print_and_log(f"Error: {e}")
            break

if __name__ == "__main__":
    main()

#                                                                                                                                                                                           38   39   40   41   42   43     44   45   46   47   48   49

# Bit (shift live)
# 0x03 0x00 0x06 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x06 0xd4 0x10 0x0e 0x00 0x00 0x00 0x48 0x00 0x00 0x01 0x01 0x00 | 0x00 0x01 0x00 0x00 0x00 0x00 | 0x00 0xff 0x02 0xc2 0x00 0x7c 0x01

# Byte (shift ended)
# 0x03 0x00 0x06 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x06 0xd4 0x10 0x0e 0x00 0x00 0x00 0x48 0x00 0x00 0x01 0x01 0x00 | 0x00 0x00 0x00 0x00 0x00 0x00 | 0x00 0xff 0x02 0xb9 0x00 0x7c 0x01

# Bit (shift ended)
# 0x03 0x00 0x06 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x06 0xd4 0x10 0x0e 0x00 0x00 0x00 0x48 0x00 0x00 0x01 0x01 0x00 | 0x00 0x01 0x00 0x00 0x00 0x00 | 0x00 0xff 0x02 0xb8 0x00 0x7c 0x01

# 0x05 0x00 0x06 0x00 0x00 0x00 0x00 0x00 0x33 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 | 0x00 0x00 0x00 0x00 0x00 0x00 | 0x00 0x00 0x00 0x00 0x00 0x00 0x00
