import pyrealsense2 as rs
import cv2
import numpy as np

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    # config.enable_stream(rs.stream.depth, 1920, 1080, rs.format.rgb8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    profile = pipeline.start(config)

    device = profile.get_device()

    
    # color_sensor = profile.get_device().query_sensors()[1]
    # color_sensor.set_option(rs.option.auto_exposure_priority, True)

    while True:
        try:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = color_frame.get_data()
            color_image = np.asanyarray(color_image)
            cv2.imshow("Color", color_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)
            break

    pipeline.stop()

if __name__ == "__main__":
    main()