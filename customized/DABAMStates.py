from common.Demonstrator import DemoState


class State000_Init(DemoState):
    def execute(self):
        self.demo_box.reset()
