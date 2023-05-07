import os
import platform
import subprocess
import sys

def main():
    system = platform.system()

    if system == "Linux":
        subprocess.run(["sudo", "usermod", "-aG", "video", os.getlogin()])

        v4l2_output = subprocess.check_output(["v4l2-ctl", "--list-devices"]).decode("utf-8")
        camera_device = v4l2_output.split("(\/dev\/video")[1].split(")")[0]

        if not camera_device:
            print("No camera device found.")
            sys.exit(1)

        os.environ["VIDEO_DEVICE"] = f"/dev/video{camera_device}"
    elif system == "Windows":
        try:
            import pydirectshow
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "pydirectshow"])

        import pydirectshow
        camera_device = pydirectshow.enumerate_devices()[0][0]

        if not camera_device:
            print("No camera device found.")
            sys.exit(1)

        os.environ["VIDEO_DEVICE"] = f"\\\\.\\pipe\\video{camera_device}"
    else:
        print("Unsupported OS.")
        sys.exit(1)

    print(f"Using camera device: {os.environ['VIDEO_DEVICE']}")

    subprocess.run(["docker-compose", "up"])

if __name__ == "__main__":
    main()
