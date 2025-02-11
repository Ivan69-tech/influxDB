import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from datetime import datetime


def conversion_time(last_successful_time):
    if isinstance(last_successful_time, datetime):
        return last_successful_time.strftime("%Y-%m-%dT%H:%M:%SZ")  
    return last_successful_time  


REMOTE_BUCKET = "distant-v2"
REMOTE_ORG = "test"
REMOTE_TOKEN = "zepvknejzovnzjenvornz"
REMOTE_URL = "http://influxdb.ivan-app.fr"

LOCAL_BUCKET = "modbus"
LOCAL_ORG = "organisation"
LOCAL_TOKEN = "tokentest"
LOCAL_URL = "http://localhost:8086"

client_remote = influxdb_client.InfluxDBClient(url=REMOTE_URL, token=REMOTE_TOKEN, org=REMOTE_ORG)
client_local = influxdb_client.InfluxDBClient(url=LOCAL_URL, token=LOCAL_TOKEN, org=LOCAL_ORG)

write_api = client_remote.write_api(write_options=SYNCHRONOUS)
query_api = client_local.query_api()

last_successful_time = "-30s"  

while True:
    try:
        last_successful_time_str = conversion_time(last_successful_time)
        print(f"Tentative de synchronisation depuis {last_successful_time_str}...")

        query = f"""
        from(bucket: "{LOCAL_BUCKET}")
        |> range(start: {last_successful_time_str})
        |> filter(fn: (r) => r["_measurement"] == "modbus")
        |> filter(fn: (r) => r["_field"] == "registre-100")
        |> sort(columns: ["_time"])  
        """

        result = query_api.query(org=LOCAL_ORG, query=query)

        data_sent = False
        for table in result:
            for record in table.records:
                field = record.get_field()
                value = int(record.get_value())  
                timestamp = record.get_time()

                p = influxdb_client.Point("Modbus").field(field, value).time(timestamp)
                write_api.write(bucket=REMOTE_BUCKET, org=REMOTE_ORG, record=p)
                print(f"Donnée envoyée [{timestamp}] : {field} = {value}")

                last_successful_time = timestamp
                data_sent = True

        if not data_sent:
            print("Aucune nouvelle donnée à envoyer.")

    except influxdb_client.rest.ApiException as e:
        print(f"Erreur InfluxDB distante : {e}")
        print("Attente avant une nouvelle tentative...")

    except Exception as e:
        print(f"Erreur inconnue : {e}")

    time.sleep(5)
