#!/bin/bash

# Function to download and set up the library
download_library() {
  local repo_name=$1
  local asset_prefix=$2
  local mpy_file_name=$3

  # Fetch the latest version tag from GitHub API
  local latest_version
  latest_version=$(curl -s "https://api.github.com/repos/adafruit/$repo_name/releases/latest" | grep -oP '"tag_name": "\K(.*)(?=")')

  if [ -z "$latest_version" ]; then
    echo "Error: Could not fetch the latest version for $repo_name. Exiting."
    exit 1
  fi

  # Construct asset name and download URL
  local asset_file="${asset_prefix}-${version_suffix}-mpy-${latest_version}.zip"
  local download_url="https://github.com/adafruit/$repo_name/releases/download/${latest_version}/${asset_file}"

  echo "Downloading $mpy_file_name from $download_url"
  curl -s -L -o "$asset_file" "$download_url"

  if [ ! -f "$asset_file" ]; then
    echo "Error: Failed to download $asset_file. Exiting."
    exit 1
  fi

  # Unzip and forcefully move the `.mpy` file to the lib directory
  if [[ "$repo_name" == "Adafruit_CircuitPython_HID" ]]; then
    # Extract only the .mpy files for the HID library
    unzip -oq "$asset_file" "*.mpy" -d "Photobooth_Pi_Pico_W_HTTP_client/lib/adafruit_hid"
  else
    # Extract only the specified .mpy file for other libraries
    unzip -oq -j "$asset_file" "**/${mpy_file_name}" -d "Photobooth_Pi_Pico_W_HTTP_client/lib"
  fi

  if [ $? -ne 0 ]; then
    echo "Error: Failed to extract $mpy_file_name. Exiting."
    exit 1
  fi

  rm -f "$asset_file"

  # Append the library name and version to library_info.txt
  echo "$mpy_file_name: $latest_version" >> Photobooth_Pi_Pico_W_HTTP_client/library_info.txt
}

# Prompt the user to select CircuitPython version
echo "Select your installed CircuitPython version to download required libraries:"
echo "1) 9.x"
echo "2) 8.x"
read -p "Enter your choice (1 or 2): " version_choice

# Validate the version selection
if [[ "$version_choice" == "1" ]]; then
  version_suffix="9.x"
elif [[ "$version_choice" == "2" ]]; then
  version_suffix="8.x"
else
  echo "Invalid selection. Please choose 1 or 2."
  exit 1
fi

# Create the target directory and the `lib` sub-directory, forcefully if needed
mkdir -p Photobooth_Pi_Pico_W_HTTP_client/lib

# Create or overwrite the library_info.txt file
echo "Library Information - Downloaded Libraries and Versions" > Photobooth_Pi_Pico_W_HTTP_client/library_info.txt
echo "------------------------------------------------------" >> Photobooth_Pi_Pico_W_HTTP_client/library_info.txt

# Download necessary libraries quietly and place them in the `lib` folder, replacing if they exist
download_library "Adafruit_CircuitPython_ConnectionManager" "adafruit-circuitpython-connectionmanager" "adafruit_connection_manager.mpy"
download_library "Adafruit_CircuitPython_Debouncer" "adafruit-circuitpython-debouncer" "adafruit_debouncer.mpy"
download_library "Adafruit_CircuitPython_Requests" "adafruit-circuitpython-requests" "adafruit_requests.mpy"
download_library "Adafruit_CircuitPython_Ticks" "adafruit-circuitpython-ticks" "adafruit_ticks.mpy"
download_library "Adafruit_CircuitPython_HID" "adafruit-circuitpython-hid" ""

# Prompt for Wi-Fi credentials and create `settings.toml`
echo "Please enter the Wi-Fi credentials to connect your Raspberry Pi Pico with your local network."
read -p "Enter Wi-Fi SSID: " wifi_ssid
read -p "Enter Wi-Fi Password: " wifi_password
echo ""

# Check for empty Wi-Fi credentials
if [[ -z "$wifi_ssid" || -z "$wifi_password" ]]; then
  echo "Error: Wi-Fi SSID and Password cannot be empty. Exiting."
  exit 1
fi

# Create `settings.toml` with Wi-Fi details, overwriting if it exists
cat <<EOL > Photobooth_Pi_Pico_W_HTTP_client/settings.toml
CIRCUITPY_WIFI_SSID = "$wifi_ssid"
CIRCUITPY_WIFI_PASSWORD = "$wifi_password"
EOL

echo "Created/Updated Photobooth_Pi_Pico_W_HTTP_client/settings.toml."

# Prompt for server IP and port
read -p "Enter the Remotebuzzer server IP (e.g., 192.168.1.100): " server_ip
read -p "Enter the Remotebuzzer server Port (e.g., 14711): " server_port

# Validate server IP and port inputs
if [[ -z "$server_ip" || -z "$server_port" ]]; then
  echo "Error: Server IP and Port cannot be empty. Exiting."
  exit 1
fi

# Download `code.py` and replace if it exists
code_url="https://raw.githubusercontent.com/PhotoboothProject/Pico_W_as_remote_button_and_rotary_encoder/refs/heads/main/code.py"
curl -s -L -o Photobooth_Pi_Pico_W_HTTP_client/code.py "$code_url"

# Replace placeholders in `code.py` with entered Remotebuzzer Server IP and Port
sed -i "s/Your_Server_IP/$server_ip/g" Photobooth_Pi_Pico_W_HTTP_client/code.py
sed -i "s/Your_Server_Port/$server_port/g" Photobooth_Pi_Pico_W_HTTP_client/code.py

echo "Modified code.py with server IP and port."
echo "################"
echo "Setup complete. All files are located in the Photobooth_Pi_Pico_W_HTTP_client folder."
