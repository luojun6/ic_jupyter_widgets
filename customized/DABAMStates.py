from common.Demonstrator import DemoState


class State000_Init(DemoState):
    def execute(self):
        self.demo_box.reset()


class State001_EnterRadiosPage(DemoState):
    def execute(self):
        self.demo_box.set_radios_page()


class State002_RunDAB(DemoState):
    def execute(self):
        self.demo_box.DAB.run()


class State003_BackToHome(DemoState):
    def execute(self):
        self.demo_box.set_home_page()


class State004_EnterSettingPage(DemoState):
    def execute(self):
        self.demo_box.set_setting_page()


class State005_TryToDisableDAB(DemoState):
    def execute(self):
        self.demo_box.DAB.prompt("Try to disable DAB in [DAB setting].")


class State006_StopDAB(DemoState):
    def execute(self):
        self.demo_box.DAB.stop()


class State007_DABEnergySaving(DemoState):
    def execute(self):
        if (
            self.demo_box.DAB.enable_setting_button.value
            == self.demo_box.DAB.DAB_DISABLED
        ):
            self.demo_box.DAB.prompt("Now it is in [DAB Energy Saving Mode].")
        else:
            self.demo_box.DAB.prompt("Now system is stopping and disabling DAB.")
            self.demo_box.DAB.stop()
            self.demo_box.DAB.enable_setting_button.value = (
                self.demo_box.DAB.DAB_DISABLED
            )
