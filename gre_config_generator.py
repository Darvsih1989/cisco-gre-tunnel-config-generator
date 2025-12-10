import pandas as pd
import os
import ipaddress

# Function to safely get a value from the dataframe
def get_cell_value(df, row, column_name):
    try:
        value = str(df.at[row, column_name]).strip()
        if pd.isna(value) or value.lower() == "nan":
            raise ValueError(f"Error: Missing value in column '{column_name}' at row {row + 1}")
        return value
    except Exception as e:
        print(e)
        exit(1)

# Function to subtract 1 from the last octet of an IP address
def decrement_last_octet(ip):
    try:
        ip_obj = ipaddress.IPv4Address(ip)
        new_ip = ipaddress.IPv4Address(int(ip_obj) - 1)
        return str(new_ip)
    except ipaddress.AddressValueError:
        print(f"Error: Invalid IP address format '{ip}'")
        exit(1)

# Load the Excel file
file_path = r"C:\Users\Public\Documents\cashless.xlsx"  # Change this to your actual file path

# Check if file exists
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found. Please check the file path.")
    exit(1)

# Try to read the Excel file with the correct engine
try:
    df = pd.read_excel(file_path, engine="openpyxl")  # Use openpyxl for .xlsx files
    df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces in column names
except ValueError as e:
    print(f"Error: {e}. This might indicate an issue with the file format or file extension.")
    exit(1)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit(1)

# Print column names and first few rows to inspect the data
print("Columns in the Excel file:", df.columns)
print("First few rows of the file:")
print(df.head())

# Ask user for row number
try:
    row_num = int(input("Enter the row number to select variables from Excel: ")) - 1  # Adjust for zero-based index
    if row_num < 0 or row_num >= len(df):
        raise ValueError("Error: Row number is out of range.")
except ValueError as e:
    print(e)
    exit(1)

# Adjusted column names based on the data you provided
var2_original = get_cell_value(df, row_num, "LOCAL GRE IP ADDRESS")  # Tunnel IP Address
var3 = get_cell_value(df, row_num, "WAN IP")  # Tunnel Destination IP
var4_original = get_cell_value(df, row_num, "LAN IP")  # Route Destination Network
var5 = get_cell_value(df, row_num, "Branch")  # Branch column

# Decrement last octet for var2 and var4
var2 = decrement_last_octet(var2_original)
var4 = decrement_last_octet(var4_original)

# Ensure var5 is an integer without the decimal part
try:
    var5_int = str(int(float(var5)))  # Convert to float first in case it's like "186.0" then to int
except ValueError:
    print(f"Error: Invalid value for Branch '{var5}'")
    exit(1)

# Ask user to manually input other variables
var0 = input("Enter Tunnel Interface Number (e.g., 30201): ").strip()
var1 = input("Enter Description Name (e.g., Abbas_Rahmati_10170): ").strip()

# Ensure manual inputs are not empty
if not var0 or not var1:
    print("Error: Tunnel Interface Number and Description cannot be empty.")
    exit(1)

# Configuration template with formatted variables
config = f"""
conf term

int Tu{var0}
description *** Cashless_{var1}_{var5_int} ***

ip flow monitor Tejarat input
ip flow monitor Tejarat output

ip address {var2} 255.255.255.252
ip mtu 1400

keepalive 10 3 

tunnel source 10.17.2.114
tunnel destination {var3}

exit

ip route {var4} 255.255.255.192 Tu{var0}

exit
"""

# Save to a file with the updated var5_int
output_file = f"{var0}_{var1}_{var5_int}_config.txt"
with open(output_file, "w") as file:
    file.write(config)

# Display results
print("\n✅ Generated Configuration:\n")
print(config)
print(f"✅ Configuration saved to '{output_file}'")
