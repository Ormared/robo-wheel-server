import cv2
import pyrealsense2 as rs
import numpy as np

def Camera(child_conn, take_pic, frame_num, camera_status):
    """
    :param child_conn: mp.Pipe for image
    :param take_pic: take pic command, 0 for rest, 1 for take one pic, after taken is 2, log file will turn back to 0
    :param frame_num: mp.Array for frame number
    :param camera_status: 0 for rest, 1 for running, 99 for end
    :return:
    """
    print('camera start')
    try:
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)
        config.enable_stream(rs.stream.color, 1920, 1080, rs.format.rgb8, 6)
        profile = pipeline.start(config)

        device = profile.get_device() # get record device
        recorder = device.as_recorder()
        recorder.pause() # and pause it

        # set frame queue size to max
        sensor = profile.get_device().query_sensors()
        for x in sensor:
            x.set_option(rs.option.frames_queue_size, 32)
        # set auto exposure but process data first
        color_sensor = profile.get_device().query_sensors()[1]
        color_sensor.set_option(rs.option.auto_exposure_priority, True)
        camera_status.value = 1
        while camera_status.value != 99:
            if take_pic.value == 3:
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()


            elif take_pic.value == 1:
                recorder.resume()
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                var = rs.frame.get_frame_number(color_frame)
                vard = rs.frame.get_frame_number(depth_frame)
                frame_num[:] = [var, vard]
                time.sleep(0.15)
                recorder.pause()
                print('taken', frame_num[:])
                take_pic.value = 2
            
            depth_color_frame = rs.colorizer().colorize(depth_frame)
            depth_image = np.asanyarray(depth_color_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            
            depth_colormap_resize = cv2.resize(depth_image, (300,200))
            color_cvt = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
            color_cvt_2 = cv2.resize(color_cvt, (300,200))
            images = np.vstack((color_cvt_2, depth_colormap_resize))
            child_conn.send(images)

        pipeline.stop()

    except RuntimeError:
        print ('run')

    finally:
        print('pipeline closed')
        camera_status.value = 98