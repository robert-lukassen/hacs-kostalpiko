# kostalpiko-sensor-hacs
A custom component to get the readings of a Kostal Piko inverter using a TCP based protocol on port 81.

The protocol offers the same information as that shown on the main webpage, with a number of additional measurments available (notably, power).

The only parameter required is the IP address of the inverter. You do not need the password.

This custom_component has config flow (Configuration from GUI) and async support and adds your inverter as a device in Home-Assistant.

Entities are configured to record long-term-data, therefore they can be used in your energy dashboard, too.

Search "Kostal" in the integrations page for setup. Please deleted old configuration from your configuration.yaml before. 

## Available options in GUI
```
current_power, total_energy, daily_energy, status

dc_<n>_voltage, dc_<n>_current, dc_<n>_power; for n = 1,2 and 3
ac_<n>_voltage, ac_<n>_current, ac_<n>_power; for n = 1,2 and 3
```

![Alt text](https://github.com/robert-lukassen/kostalpiko-sensor-homeassistant/blob/master/img/Schermafbeelding%202020-03-30%20om%2011.25.18.png?raw=true "Optional Title")

## configuration.yaml

```
sensor:
  - platform: kostalpiko
    host: !secret kostalpiko_host  # "http://192.168.xx.xx"
    monitored_conditions:
      - status
      - current_power
      - total_energy
      - daily_energy
      - dc_1_voltage
      - dc_1_current
      - dc_1_power
      - dc_2_voltage
      - dc_2_current
      - dc_2_power
      - dc_3_voltage
      - dc_3_current
      - dc_3_power
      - ac_1_voltage
      - ac_1_current
      - ac_1_power
      - ac_2_voltage
      - ac_2_current
      - ac_2_power
      - ac_3_voltage
      - ac_3_current
      - ac_3_power
```
