import routeros_api
import time
import pygame
# MikroTik router connection details
ROUTER_IP = '192.168.100.100'  # Replace with your router's IP
USERNAME = 'admin'           # Replace with your router username
PASSWORD = 'password'        # Replace with your router password
TARGET_IP = '192.168.50.253'  # The specific IP to monitor
TRAFFIC_THRESHOLD = 100000   # Traffic threshold in bytes (100KB)



def play_sound():
    pygame.mixer.init()

    # Load and play sound
    pygame.mixer.music.load('alarm.mp3')
    pygame.mixer.music.play()

# Keep the script running while the sound is playing
    while pygame.mixer.music.get_busy():
        pass
# Connect to the MikroTik router
def connect_to_router():
    try:
        connection = routeros_api.RouterOsApiPool(
            ROUTER_IP, username=USERNAME, password=PASSWORD, plaintext_login=True
        )
        return connection.get_api()
    except Exception as e:
        print(f"Failed to connect to the router: {e}")
        return None

# Monitor traffic for a specific IP
def monitor_ip_traffic(api):
    try:
        connections = api.get_resource('/ip/firewall/connection')

        while True:
            print("Scanning for traffic...")
            active_connections = connections.get()
           
            for i in range(len(active_connections)):
                if TARGET_IP in active_connections[i]['src-address']:
                    connection_bytes = int(active_connections[i]['repl-bytes'])
                    if connection_bytes > TRAFFIC_THRESHOLD:
                        play_sound()

            time.sleep(5)  # Wait for 5 seconds before scanning again
    except Exception as e:
        print(f"Error monitoring traffic: {e}")

# Main function
def main():
    api = connect_to_router()
    if not api:
        return

    monitor_ip_traffic(api)

if __name__ == '__main__':
    main()

