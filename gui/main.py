from kivy.app import App, Widget
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.core.image import Image
import kivy
kivy.require('2.3.0')


class MyCamera(Widget):
    def __init__(self, **kwargs):
        super(MyCamera, self).__init__(**kwargs)
        self.camera: Camera = self.ids['camera']
        self.btn: Button = self.ids['capture_btn']

    def capture_image(self):
        self.camera.export_to_png(f'capture_low.png')
        tex: Image = self.camera.texture
        tex.save('capture_high.png')
        print('Captured')


class CamApp(App):
    def build(self):
        return MyCamera()


if __name__ == '__main__':
    kivy.Config.set('graphics', 'width', '480')
    kivy.Config.set('graphics', 'height', '320')
    kivy.Config.set('graphics', 'resizable', '0')
    # kivy.Config.set('graphics', 'fullscreen', '1')
    CamApp().run()
