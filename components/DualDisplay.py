import json
import os
import threading
import ipywidgets as widgets
from IPython.core.display import display

from utils.files_mgmt import res_dir


# Copy this html to jupyter notebook
JUPYTER_HTML = """
%%html
<style>
.screen_off{
    background-color:black;
}
.theme_day{
    background-color:#F9F9F9;
}
.theme_night{
    background-color:#1E1E1E;
}
</style>
"""


class GeneralDisplay(widgets.HBox):
    WIDTH = "50%"
    HEIGHT = "160px"
    SCREEN_OFF = "screen_off"
    THEME_NIGHT = "theme_night"
    THEME_DAY = "theme_day"
    DRIVER_DISPLAY_POWERUP_DURATION = 0.3
    DRIVER_DISPLAY_STARTUP_DURATION = 0.3
    CENTRAL_DISPLAY_POWERUP_DURATION = 0.6
    CENTRAL_DISPLAY_STARTUP_DURATION = 3
    DEAFAULT_GENERAL_USERDB_PATH = os.path.join(res_dir, "db/general_userdb.json")

    THEME_DAY_NIGHT_SETTING = "theme_day_night_setting"

    def __init__(
        self,
        # children,
        power_up_duration=0.5,
        start_up_duration=1,
        userdb_path=DEAFAULT_GENERAL_USERDB_PATH,
        **kwargs
    ):
        self.__power_up_duration = power_up_duration
        self.__power_up_event = threading.Event()
        self.__power_up_timer = threading.Timer(
            self.__power_up_duration, self.__power_up_callback, [self.__power_up_event]
        )

        self.__start_up_duration = start_up_duration
        self.__start_up_event = threading.Event()
        self.__start_up_timer = threading.Timer(
            self.__start_up_duration, self.__start_up_callback, [self.__start_up_event]
        )

        self.__userdb_path = userdb_path
        with open(self.__userdb_path, "r+") as userdb:
            # self.__userdb = userdb
            self.__user_setting = json.load(userdb)

        self.__background = self.SCREEN_OFF
        self.add_class(self.__background)

        self.__forground = widgets.Output(
            layout=widgets.Layout(justify_content="center", align_items="center")
        )

        self.__html = widgets.HTML()

        super().__init__([self.__forground], **kwargs)

    def save_userdb(self, key=None, value=None):
        if key:
            self.__user_setting[key] = value
        with open(self.__userdb_path, "w+") as userdb:
            json.dump(self.__user_setting, userdb)

    @property
    def forground(self):
        return self.__forground

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value=""):
        if value:
            # print(self.__background.replace("theme", "font_color"))
            self.__html.add_class(self.__background.replace("theme", "font_color"))
        self.__html.value = value

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, background: str):
        self.remove_class(self.__background)
        self.__background = background
        self.add_class(self.__background)

    # Ready to override
    def start_up(self):
        self.html = "<h3>System is starting up....</h3>"
        with self.__forground:
            display(self.__html)
        self.__start_up_timer.start()
        try:
            self.__start_up_event.wait(self.__start_up_duration)
        finally:
            pass

    # Ready to override
    def start_up_callback(self):
        pass

    def power_up(self):
        self.__power_up_timer.start()
        try:
            self.__power_up_event.wait(self.__power_up_duration)
        finally:
            # self.start_up()
            pass

    def __power_up_callback(self, event):
        event.set()
        if self.__user_setting[self.THEME_DAY_NIGHT_SETTING]:
            self.__background = self.__user_setting[self.THEME_DAY_NIGHT_SETTING]
        else:
            self.__background = self.THEME_NIGHT
        self.background = self.__background
        self.start_up()

    def __start_up_callback(self, event):
        event.set()
        self.__forground.clear_output()
        self.html = ""
        self.start_up_callback()


class DriverDisplay(GeneralDisplay):
    def __init__(self, **kwargs):
        self.layout = widgets.Layout(
            justify_content="space-around",
            width=self.WIDTH,
            height=self.HEIGHT,
            border="solid",
            align_items="center",
        )
        self.__left_display = widgets.Output()
        # self.__central_display = widgets.Output()
        self.__right_display = widgets.Output()

        super().__init__(**kwargs)
        self.children = [self.__left_display, self.forground, self.__right_display]


class DockButton(widgets.Button):
    def __init__(self, icon: str, button_style="info", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.button_style = button_style
        self.layout = widgets.Layout(width="auto")


class CentralDisplay(GeneralDisplay):
    def __init__(self, **kwargs):
        self.layout = widgets.Layout(
            justify_content="flex-start",
            width=self.WIDTH,
            height=self.HEIGHT,
            border="solid",
            align_items="center",
        )
        self.__home_button = DockButton(icon="home")
        self.__setting_button = DockButton(icon="gear")
        self.__car_button = DockButton(icon="car")
        self.__bars_button = DockButton(icon="bars")
        self.__dock_buttons = widgets.VBox(
            [
                self.__home_button,
                self.__setting_button,
                self.__car_button,
                self.__bars_button,
            ]
        )

        self.__dock_buttons.layout = widgets.Layout(padding="3px")
        self.__dock = widgets.Output()
        # self.__forground = widgets.Output()

        super().__init__(**kwargs)
        self.children = [self.__dock, self.forground]

    def start_up_callback(self):
        with self.__dock:
            display(self.__dock_buttons)

        return super().start_up_callback()


class DualDisplay(widgets.HBox):
    def __init__(
        self,
        driver_display_powerup_duration=GeneralDisplay.DRIVER_DISPLAY_POWERUP_DURATION,
        driver_display_startup_duration=GeneralDisplay.DRIVER_DISPLAY_STARTUP_DURATION,
        central_display_powerup_duration=GeneralDisplay.CENTRAL_DISPLAY_POWERUP_DURATION,
        central_display_startup_duration=GeneralDisplay.CENTRAL_DISPLAY_STARTUP_DURATION,
        **kwargs
    ):
        self.__driver_display = DriverDisplay(
            power_up_duration=driver_display_powerup_duration,
            start_up_duration=driver_display_startup_duration,
        )
        self.__central_display = CentralDisplay(
            power_up_duration=central_display_powerup_duration,
            start_up_duration=central_display_startup_duration,
        )
        super().__init__([self.__driver_display, self.__central_display], **kwargs)

    @property
    def driver_display(self):
        return self.__driver_display

    @property
    def central_display(self):
        return self.__central_display

    def power_up(self):
        self.__driver_display.power_up()
        self.__central_display.power_up()
