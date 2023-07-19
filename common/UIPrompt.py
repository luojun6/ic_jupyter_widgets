import ipywidgets as widgets
import threading


class UIPrompt(widgets.Text):
    def __init__(self, prompt_duration=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.description = "Prompt: "
        self.value = ""
        self.__duration = prompt_duration
        self.__reset_event = threading.Event()
        self.__timer = threading.Timer(
            self.__duration, self.__timer_callback, [self.__reset_event]
        )

    def prompt(self, message: str):
        self.value = message
        self.__timer.start()
        try:
            self.__reset_event.wait(self.__duration)
        finally:
            self.__init__()

    def __timer_callback(self, event):
        self.value = ""
        event.set()
        # self.__init__()
