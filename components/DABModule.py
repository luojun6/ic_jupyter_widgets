import ipywidgets as widgets
from common.UIPrompt import UIPrompt


class DABModule(widgets.VBox):
    DAB_ENABLED = "DAB_ENABLED"
    DAB_DISABLED = "DAB_DISABLED"
    DAB_STATUS = [DAB_ENABLED, DAB_DISABLED]
    DAB_RUN_STATUS = "DAB is running."
    DAB_STOP_STATUS = "DAB is not runing."

    def __init__(self, **kwargs):
        self.__running_status = False

        self.__enabler = widgets.ToggleButton(
            value=True,
            description="Digital Audio Boardcasting",
            layout={"width": "300px", "height": "60px"},
            icon="radio",
            button_style="warning",
        )
        self.__enabler_status = widgets.ToggleButtons(
            options=self.DAB_STATUS,
            value=self.DAB_ENABLED,
            # description="DAB Status",
            # button_style="warning",
            tooltips=["Click to disable DAB", "Click to enable DAB"],
        )
        self.__run_button = widgets.Button(
            # value=False,
            description=self.DAB_STOP_STATUS,
            layout={"width": "300px", "height": "30px"},
            icon="star",
            button_style="",
        )

        self.__prompt = UIPrompt(prompt_duration=2)

        super().__init__(
            [self.__enabler, self.__enabler_status, self.__run_button, self.__prompt],
            **kwargs
        )

        self.__enabler.observe(self.__on_change_enabler, "value")
        self.__enabler_status.observe(self.__on_change_enable_status, "value")
        self.__run_button.on_click(self.__on_click_run_button)

    def __on_change_enable_status(self, change):
        if change["new"] is self.DAB_ENABLED:
            self.__enabler.value = True

        else:
            self.__enabler.value = False

    def __on_change_enabler(self, change):
        if change["new"]:
            self.__enabler.button_style = "warning"

            if self.__enabler_status.value is self.DAB_DISABLED:
                self.__enabler_status.value = self.DAB_ENABLED

        else:
            if self.__running_status:
                self.__prompt.prompt("Disabling is not allowed while DAB is running!")
                self.__enabler.value = True
                return

            self.__enabler.button_style = ""

            if self.__enabler_status.value is self.DAB_ENABLED:
                self.__enabler_status.value = self.DAB_DISABLED

    def __on_click_run_button(self, btn: widgets.Button):
        if self.__running_status:
            self.__running_status = False
            btn.description = self.DAB_STOP_STATUS
            btn.button_style = ""

        else:
            self.__running_status = True
            btn.description = self.DAB_RUN_STATUS
            btn.button_style = "info"

            if self.__enabler_status.value is self.DAB_DISABLED:
                self.__enabler_status.value = self.DAB_ENABLED

    def run(self):
        self.__running_status = True
        self.__run_button.description = self.DAB_RUN_STATUS
        self.__run_button.button_style = "info"
        self.__enabler_status.value = self.DAB_ENABLED

    def stop(self):
        self.__running_status = False
        self.__run_button.description = self.DAB_STOP_STATUS
        self.__run_button.button_style = ""

    @property
    def enable_setting_button(self):
        return self.__enabler_status

    @property
    def run_button(self):
        return self.__run_button

    @property
    def running_status(self):
        return self.__running_status

    # @property
    def prompt(self, message: str):
        self.__prompt.prompt(message)
