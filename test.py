import time

while Exception as e:
    try:
        print("hello")
        time.sleep(1)
    except Exception as e:
        print(f"Error occurred: {e}")
        break
