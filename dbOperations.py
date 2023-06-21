from dotenv import load_dotenv
import os
import psycopg2


def create_table(table_values):
    load_dotenv()
    hostname = os.environ.get("hostname")
    database = os.environ.get("database")
    username = os.environ.get("username")
    password = os.environ.get("password")
    port_id = os.environ.get("port_id")
    connect = os.environ.get("connect")

    with psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=password,
        port=port_id
    ) as connect:
        cursor = connect.cursor()

        cursor.execute("DROP TABLE IF EXISTS device_interface_config")

        create_script = """ CREATE TABLE device_interface_config 
                                (id SERIAL PRIMARY KEY,
                                connection INTEGER,
                                name VARCHAR(255) NOT NULL,
                                description VARCHAR(255),
                                config json,
                                type VARCHAR(50),
                                infra_type VARCHAR(50),
                                port_channel_id INTEGER,
                                max_frame_size INTEGER)"""
        cursor.execute(create_script)

        insert_script = """INSERT INTO device_interface_config 
        (id, connection, name, description, config, type, 
        infra_type, port_channel_id, max_frame_size) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        for record in table_values:
            cursor.execute(insert_script, record)

    connect.close()
