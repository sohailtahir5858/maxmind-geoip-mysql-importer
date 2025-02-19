# GeoIP to MySQL Importer

This Python script reads data from a `.mmdb` file (MaxMind GeoIP database) and imports it into a MySQL database. I created it for a usecase of filtering requests from certain countries. we didn't want to use external ip so we created an efficient database structure to store all the ip ranges and filter the incoming request based on this record. It is designed to handle IPv4 addresses, skip IPv6 addresses, and avoid duplicate entries in the database.

## Features

- Reads `.mmdb` files (MaxMind GeoIP format).
- Imports IP ranges, country codes, country names, and geoname IDs into a MySQL table.
- Skips IPv6 addresses and invalid IP ranges.
- Prevents duplicate entries using a unique constraint on IP ranges.
- Easy to set up and run.

---

## Prerequisites

Before running the script, ensure you have the following installed:

1. **Python 3.8+**
2. **MySQL Server**
3. **Required Python Libraries**:
   - `mysql-connector-python`
   - `maxminddb`
   - `ipaddress`

You can install the required libraries using `pip`:

```bash
pip install mysql-connector-python maxminddb
```
## Setup

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/geoip-to-mysql.git
cd geoip-to-mysql
```

### 2. Prepare the .mmdb File

Download the latest .mmdb file from MaxMind (e.g., GeoLite2 Country) or use the one attached in the project directory.

### 3. Configure MySQL

Create a MySQL database and update the configuration in the script:

```bash
mysql_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'logomaker-imagine'
}
```

Replace the placeholders with your MySQL credentials.

## Database Schema

The script creates a table named geoip with the following schema:

```bash
CREATE TABLE IF NOT EXISTS geoip (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_range_start VARCHAR(45) NOT NULL,
    ip_range_end VARCHAR(45) NOT NULL,
    geoname_id INT,
    country_iso_code VARCHAR(2),
    country_name VARCHAR(255),
    UNIQUE KEY unique_ip_range (ip_range_start, ip_range_end)
);
```
- ip_range_start: Start of the IP range.
- ip_range_end: End of the IP range.
- geoname_id: Geoname ID of the country.
- country_iso_code: ISO code of the country (e.g., AU for Australia).
- country_name: Name of the country in English.

## Execution

### 1. Run the Script

 Run the script using Python:

```bash
python geoip_to_mysql.py
```
### 2. Expected Output

The script will:

- Create the geoip table (if it doesn’t exist).
- Read the .mmdb file and insert data into the MySQL table.
- Skip IPv6 addresses and invalid IP ranges.
- Log progress and errors to the console.

### Example output:
```bash
Table 'geoip' created or already exists.
Skipping IPv6 address: 2001:200::
Inserted data for IP range: 223.255.255.0 - 223.255.255.255
Skipping duplicate IP range: 223.255.255.0 - 223.255.255.255
Data inserted successfully.
MySQL connection closed.
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- MaxMind for providing the GeoIP databases.
- Python ipaddress module for IP address handling.
