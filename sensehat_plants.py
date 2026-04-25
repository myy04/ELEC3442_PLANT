import os
import json
import time
import base64
import mimetypes
from datetime import datetime, timezone

from sense_hat import SenseHat
from picamera2 import Picamera2

OUTPUT_JSON_PATH = "plant_data.json"
CAPTURED_IMAGE_PATH = "/home/rancesama/plants/captured_photos/captured_plant.jpg"


def get_current_time():
    return datetime.now(timezone.utc).isoformat()


def capture_photo(image_path):
    picam2 = Picamera2()

    # Configure camera for still image capture
    config = picam2.create_still_configuration()
    picam2.configure(config)

    picam2.start()

    # Give the camera a short time to adjust exposure/white balance
    time.sleep(2)

    picam2.capture_file(image_path)
    picam2.stop()
    picam2.close()

    return image_path


def encode_image_to_base64(image_path):
    if not os.path.exists(image_path):
        return None

    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return {
        "filename": os.path.basename(image_path),
        "mime_type": mime_type,
        "data": encoded
    }


def main():
    sense = SenseHat()

    captured_image_path = capture_photo(CAPTURED_IMAGE_PATH)

    data = {
        "current_time": get_current_time(),
        "temperature": round(sense.get_temperature(), 2),
        "humidity": round(sense.get_humidity(), 2),
        "image_data": encode_image_to_base64(captured_image_path)
    }

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
