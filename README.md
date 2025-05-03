# Home Assistant IPMI Control Integration

This custom integration for Home Assistant allows you to monitor and control servers that support the Intelligent Platform Management Interface (IPMI).

## Features

* Retrieves power consumption (in Watts).
* Retrieves server temperature (in Celsius).
* Allows sending power commands:
    * Power Up
    * Power Down
    * Power Reset

## Installation

### Via HACS (Home Assistant Community Store)

1.  Ensure that HACS is installed in your Home Assistant instance.
2.  Go to the HACS panel in Home Assistant.
3.  Click on the "+" button in the bottom right corner.
4.  Add the following repository URL: `https://github.com/@yoyo1637/homeassistant-ipmi-control` (Replace with your actual GitHub username and repository name)
5.  Select the "Integration" category and click "Add".
6.  After the integration is downloaded, restart Home Assistant.

### Manual Installation

1.  Download the latest release of this integration from GitHub.
2.  Extract the contents of the release ZIP file.
3.  Copy the `ipmi_control` folder into the `custom_components` directory of your Home Assistant configuration (e.g., `/config/custom_components/`).
4.  Restart Home Assistant.

## Configuration

1.  Go to "Settings" -> "Devices & Services" in your Home Assistant interface.
2.  Click on the "+ Add Integration" button.
3.  Search for "IPMI Control" and click on it.
4.  You will be prompted to enter the details of your IPMI server:
    * **Host:** The IP address or hostname of your IPMI interface.
    * **Username:** The username for your IPMI interface.
    * **Password:** The password for your IPMI interface.
    * **Port:** (Optional) The port number for IPMI (default is 623).
5.  Click "Submit". You can add multiple IPMI servers by repeating this process.

## Usage

Once configured, you will have new entities in Home Assistant:

* **Sensors:**
    * `sensor.nom_du_serveur_power_consumption`: Displays the current power consumption in Watts.
    * `sensor.nom_du_serveur_temperature`: Displays the server temperature in Celsius.
* **Switches:**
    * `switch.nom_du_serveur_power_up`: Sends the power up command to the server.
    * `switch.nom_du_serveur_