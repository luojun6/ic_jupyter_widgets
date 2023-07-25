import ipywidgets as widgets
from IPython.core.display import display

# from common.UIPrompt import UIPrompt
from components.Foreground import FORGROUND_PAGE_WIDTH, create_forground_image
from components.DABModule import DABModule


class DABPM(widgets.HBox):
    def __init__(self, **kwargs):
        self.__out = widgets.Output(
            layout={"border": "1px solid black", "height": "240px", "width": "320px"}
        )
        self.__home_button = widgets.Button(
            description="Home",
            icon="home",
            button_style="info",
            layout=widgets.Layout(width="50%", height="30px", margin="top"),
        )
        self.__setting_button = widgets.Button(
            description="Setting",
            icon="gear",
            button_style="info",
            layout=widgets.Layout(width="50%", height="30px", margin="top"),
        )

        self.__DAB_button = widgets.Button(
            description="DAB",
            # value=True,
            icon="star",
            button_style="info",
            layout=widgets.Layout(width="50%", height="30px", margin="top"),
        )

        self.__radio_button = widgets.Button(
            description="Radios",
            # value=True,
            icon="bars",
            button_style="info",
            layout=widgets.Layout(width="50%", height="30px", margin="top"),
        )
        self.__DAB = DABModule()

        self.__setting = widgets.Accordion(
            children=[
                self.__DAB.enable_setting_button,
                widgets.IntSlider(),
            ],
            # titles=("FakedSettingA", "FakedSettingB", "DAB Setting"),
            layout={"width": f"{FORGROUND_PAGE_WIDTH}px"},
        )
        titles = ["DAB Setting", "FakedSetting"]
        [self.__setting.set_title(i, title) for i, title in enumerate(titles)]

        self.__setting_page = widgets.VBox([self.__setting, self.__home_button])

        self.__home_page = widgets.VBox(
            [
                create_forground_image("ivi_home_example.jpg"),
                widgets.HBox([self.__radio_button, self.__setting_button]),
            ]
        )

        self.__radio_page = widgets.VBox(
            [
                create_forground_image("radio_example.jpg"),
                widgets.HBox([self.__home_button, self.__DAB_button]),
            ]
        )

        self.__home_button.on_click(self.__on_click_home_button)
        self.__radio_button.on_click(self.__on_click_radio_button)
        self.__setting_button.on_click(self.__on_click_setting_button)
        self.__DAB_button.on_click(self.__on_click_DAB_button)

        with self.__out:
            display(self.__home_page)

        # self.__prompt = UIPrompt()
        super().__init__(
            # [self.__out, widgets.VBox([self.__DAB, self.__prompt])],
            [self.__out, self.__DAB],
            **kwargs,
        )

    # def prompt(self, message: str):
    #     return self.__prompt.prompt(message)

    def reset(self):
        self.__init__()

    def set_home_page(self):
        self.__out.clear_output()
        with self.__out:
            display(self.__home_page)

    def set_radios_page(self):
        self.__out.clear_output()
        with self.__out:
            display(self.__radio_page)

    def set_setting_page(self):
        self.__out.clear_output()
        with self.__out:
            display(self.__setting_page)

    @property
    def DAB(self):
        return self.__DAB

    def __on_click_DAB_button(self, btn):
        if self.__DAB.running_status:
            self.__DAB.stop()

        else:
            self.__DAB.run()

    def __on_click_home_button(self, btn):
        self.set_home_page()

    def __on_click_radio_button(self, btn):
        self.set_radios_page()

    def __on_click_setting_button(self, btn):
        self.set_setting_page()
