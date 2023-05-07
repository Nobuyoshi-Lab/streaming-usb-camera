import platform
import subprocess
import sys

def main():
    system = platform.system()

    if system == "Linux":
        try:
            v4l2_output = subprocess.check_output(["v4l2-ctl", "--list-devices"]).decode("utf-8")
            camera_device = v4l2_output.split("(\/dev\/video")[1].split(")")[0]
        except (subprocess.CalledProcessError, IndexError):
            print("No camera device found.")
            sys.exit(1)

        video_device = f"/dev/video{camera_device}"
    else:
        print("Unsupported OS.")
        sys.exit(1)

    print(f"Using camera device: {video_device}")

    with open(".env", "w") as env_file:
        env_file.write(f"VIDEO_DEVICE={video_device}\n")

if __name__ == "__main__":
    main()
