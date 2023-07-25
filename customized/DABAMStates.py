from common.Demonstrator import DemoState


class State000_Init(DemoState):
    def execute(self):
        self.demo_box.reset()


class State001_EnterRadiosPageAtBeginning(DemoState):
    def execute(self):
        self.demo_box.set_radios_page()


class State002_RunDABAtBeginning(DemoState):
    def execute(self):
        self.demo_box.DAB.run()


class State003_BackToHomenDABRunning(DemoState):
    def execute(self):
        self.demo_box.set_home_page()


class State004_EnterSettingPage(DemoState):
    def execute(self):
        self.demo_box.set_setting_page()


class State005_TryToDisableDAB(DemoState):
    def execute(self):
        self.demo_box.DAB.prompt("Try to disable DAB in [DAB setting].")


class State006_BackToHomeOnDABRunning(DemoState):
    def execute(self):
        self.demo_box.set_home_page()


class State007_EnterRadiosPagenDABRunning(DemoState):
    def execute(self):
        self.demo_box.set_radios_page()


class State008_StopDAB(DemoState):
    def execute(self):
        self.demo_box.DAB.set_setting_page()


class State009_DisableOnDAPStopped(DemoState):
    def execute(self):
        self.demo_box.DAB.stop()
        self.demo_box.DAB.enable_setting_button.value = self.demo_box.DAB.DAB_DISABLED


# Not used
class State009_DABEnergySavingPrompt(DemoState):
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


class State010_BackToHomeOnDABStopped(DemoState):
    def execute(self):
        self.demo_box.set_home_page()


class State011_EnterRadiosPagenDABStopped(DemoState):
    def execute(self):
        self.demo_box.set_radios_page()


class State012_RunDABOnEnergySavingMode(DemoState):
    def execute(self):
        self.demo_box.DAB.run()
        self.demo_box.DAB.prompt("Now it is exiting from [DAB Energy Saving Mode].")
