
from netmiko import ConnectHandler

router = {
    "device_type": "cisco_ios",
    "ip": "10.10.11.2",
    "username": "admin",
    "password": "admin",
    "port": 22
}

net_connect = ConnectHandler(**router)
net_connect.enable()
print(f" please wait we are connect to {router['ip']}....")
    
commands = [
        "interface Gi0/0",
        "ip address 10.1.1.33 255.255.255.254",
        "description CONN TO ISP PORT Gi1/0/1",
        "no shutdown",
        "ip route 0.0.0.0 0.0.0.0 10.1.1.32"
    ]
    
output = net_connect.send_config_set(commands)
print(output)
    
print(f"Successfully configured WAN interface")

output = net_connect.send_command("show running | section ftp")
if ("ip ftp source interface loopback 0") in output:
    print("source interface configured")
    
else:
    print("ftp source interface is not configured")
    
ios_file = "c2900-universalk9-mz.SPA.157-3.M8.bin"
check_command = f"dir flash: | include {ios_file}"
output = net_connect.send_command(check_command)

if ios_file in output:
    print(f"File '{ios_file}' already exists in flash. Transfer skipped.")

else:   
    ftp_command = f"copy ftp://admin:cisco123@192.168.1.50/ios/c2900-universalk9-mz.SPA.157-3.M8.bin flash:"
    output = net_connect.send_command_timing(ftp_command, delay_factor=5)
    
if "Destination filename" in output:
    output += net_connect.send_command_timing("\n", delay_factor=5)
    print(output)
    
md5_value = "6684902555795363829"

output = net_connect.send_command_timing("verify /md5 c2900-universalk9-mz.SPA.157-3.M8.bin")
print(output)
if md5_value in output:
    print("md5 key value matched")
    
else:
    print("md5 key is not matched please re_run ios file")
    
output = net_connect.send_config_set("boot system flash:c2900-universalk9-mz.SPA.157-3.M8.bin")
print("Boot command output:\n", output)

if net_connect.check_config_mode():
    net_connect.exit_config_mode()
    print("Exited config mode")

output = net_connect.send_command_timing("write memory")
print("Write memory output:\n", output)

output = net_connect.send_command_timing("reload in 1")
if "confirm" in output.lower():
    output += net_connect.send_command_timing("\n")
    print(output)
    
net_connect.disconnect()
