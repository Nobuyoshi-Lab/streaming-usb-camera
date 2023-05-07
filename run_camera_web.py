import platform
import subprocess
import sys
import cv2

def main():
    system = platform.system()

    if system == "Linux":
        v4l2_output = subprocess.check_output(["v4l2-ctl", "--list-devices"]).decode("utf-8")
        camera_device = v4l2_output.split("(\/dev\/video")[1].split(")")[0]

        if not camera_device:
            print("No camera device found.")
            sys.exit(1)

        video_device = f"/dev/video{camera_device}"
    elif system == "Windows":
        camera_device = None
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap is None or not cap.isOpened():
                continue
            camera_device = i
            cap.release()
            break

        if camera_device is None:
            print("No camera device found.")
            sys.exit(1)

        video_device = str(camera_device)
    else:
        print("Unsupported OS.")
        sys.exit(1)

    print(f"Using camera device: {video_device}")

    with open(".env", "w") as env_file:
        env_file.write(f"VIDEO_DEVICE={video_device}\n")

if __name__ == "__main__":
    main()
