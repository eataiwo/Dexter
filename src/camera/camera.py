import io
import time
import picamera
from camera.base_camera import BaseCamera


class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera(resolution=(640, 480), framerate=12) as camera:
            # let camera warm up
            camera.video_stabilization = True
            time.sleep(0)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                               use_video_port=True, resize=(640,360)):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

# https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
