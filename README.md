📌 Project: Cashless Config Generator

Python script for generating Cisco GRE Tunnel configurations automatically using data from an Excel file.
This tool helps network engineers automate the creation of standard tunnel configuration templates by selecting variables directly from an .xlsx file.


---

🚀 Features

Load Excel file containing GRE, WAN, LAN, and Branch info

Validate all fields and prevent missing / invalid data

Automatically decrement last octet of IPs

Ask user to input Tunnel Interface Number & Description

Generate full Cisco Tunnel + Route configuration

Automatically save output as:

<TunnelNumber>_<Description>_<Branch>_config.txt



---

📁 Project Structure

cashless-config-generator/
│── script.py
│── sample_cashless.xlsx
│── README.md


---

🧩 Excel Format (Required)

The Excel file must contain these columns exactly:

LOCAL GRE IP ADDRESS	WAN IP	LAN IP	Branch



Example rows included in sample_cashless.xlsx.


---

🛠 Requirements

Install required Python modules:

pip install pandas openpyxl ipaddress


---

▶️ How to Run the Script

1️⃣ Run the Python script

python script.py

2️⃣ The program loads the Excel file automatically from:

C:\Users\Public\Documents\cashless.xlsx

(You can change this path inside the script.)

3️⃣ Select a row from the Excel data

The script prints the table and asks:

Enter the row number to select variables from Excel:

4️⃣ Enter manual inputs

Then you will be asked for:

Enter Tunnel Interface Number (e.g., 30201)
Enter Description Name (e.g., Abbas_Rahmati_10170)


---

📄 Output Example

The script generates:

conf term

int Tu30201
description *** Cashless_Abbas_Rahmati_10170_186 ***

ip flow monitor Tejarat input
ip flow monitor Tejarat output

ip address 172.16.5.1 255.255.255.252
ip mtu 1400

keepalive 10 3
tunnel source 10.17.2.114
tunnel destination 192.168.10.5

exit

ip route 192.168.20.0 255.255.255.192 Tu30201

exit

And saves it automatically to:

30201_Abbas_Rahmati_10170_186_config.txt


---

📌 Notes

Script includes full error handling

Automatically removes .0 from Branch values (e.g., 186.0 → 186)

Stops execution if Excel values are missing or invalid

Decrements last octet safely using Python ipaddress module



---

📞 Support

If you want, you can continue expanding this project with:

GUI version

Supporting multiple tunnels

Full batch generation

