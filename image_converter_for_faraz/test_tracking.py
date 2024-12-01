import requests
import platform
import hashlib
import json

def test_tracking():
    api_url = 'https://wordpress.atz.li/pro_dds_tool_tracker/track.php'
    
    # Generate test machine ID
    system_info = f"{platform.node()}-{platform.machine()}-{platform.processor()}"
    machine_id = hashlib.md5(system_info.encode()).hexdigest()
    
    # Test data
    data = {
        'user_id': machine_id,
        'event': 'test',
        'system': platform.system(),
        'version': '1.0.0'
    }
    
    try:
        # Add headers to specify JSON content
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'DDS-Converter/1.0'
        }
        
        # Convert data to JSON string
        json_data = json.dumps(data)
        print(f"Sending data: {json_data}")
        
        response = requests.post(
            api_url, 
            data=json_data,  # Send as JSON string
            headers=headers, 
            timeout=5
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_tracking()