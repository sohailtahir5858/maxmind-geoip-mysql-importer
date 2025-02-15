import maxminddb
import mysql.connector
from mysql.connector import Error
from ipaddress import IPv4Network, IPv6Network

# Path to your .mmdb file
mmdb_path = 'GeoLite2-Country.mmdb'

# MySQL connection details
mysql_config = {
    'host': 'localhost',
    'port': 3306,
    'user': '',
    'password': '',
    'database': ''
}

# Table details
table_name = ''

# Create MySQL table
def create_table(cursor):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_range_start VARCHAR(45) NOT NULL,
    ip_range_end VARCHAR(45) NOT NULL,
    geoname_id INT,
    country_iso_code VARCHAR(2),
    country_name VARCHAR(255),
    INDEX idx_ip_range_start (ip_range_start),
    INDEX idx_ip_range_end (ip_range_end)
    );
    """
    try:
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")

# Insert data into MySQL
def insert_data(cursor, ip_range_start, ip_range_end, geoname_id, country_iso_code, country_name):
    insert_query = f"""
    INSERT INTO {table_name} (ip_range_start, ip_range_end, geoname_id, country_iso_code, country_name)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        geoname_id = VALUES(geoname_id),
        country_iso_code = VALUES(country_iso_code),
        country_name = VALUES(country_name)
    """
    try:
        cursor.execute(insert_query, (ip_range_start, ip_range_end, geoname_id, country_iso_code, country_name))
    except Error as e:
        print(f"Error inserting data: {e}")

# Main function
def main():
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Create table
        create_table(cursor)
        print("table created")

        # Open the .mmdb file
        with maxminddb.open_database(mmdb_path) as reader:
            # Iterate over all IP ranges and their data
            for network, data in reader:
                try:
                    if isinstance(network, IPv6Network):
                        print(f"Skipping IPv6 address: {network}")
                        continue
                    # Extract registered country information
                    registered_country = data.get('registered_country', {})
                    geoname_id = registered_country.get('geoname_id', None)
                    country_iso_code = registered_country.get('iso_code', None)
                    country_name = registered_country.get('names', {}).get('en', None)

                    # Extract IP range start and end
                    ip_network = IPv4Network(network)
                    ip_range_start = str(ip_network.network_address)
                    ip_range_end = str(ip_network.broadcast_address)

                    # Insert data into MySQL
                    print(ip_range_start, ip_range_end, geoname_id, country_iso_code, country_name)
                    insert_data(cursor, ip_range_start, ip_range_end, geoname_id, country_iso_code, country_name)
                except Exception as e:
                    print(f"Skipping invalid IP range: {network} - {e}")
                    continue

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    main()