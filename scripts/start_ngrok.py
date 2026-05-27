from pyngrok import ngrok
import time
import sys

print("Starting ngrok tunnel to port 8000...")
try:
    public_url = ngrok.connect(8000).public_url
    print(f"\n=======================================================")
    print(f"YOUR GLOBAL URL IS: {public_url}")
    print(f"=======================================================\n")
    print("Keep this script running to maintain the connection.")
    print("Press Ctrl+C to stop.")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping ngrok tunnel...")
        ngrok.kill()
except Exception as e:
    print(f"Error starting ngrok: {e}")
    sys.exit(1)
