from __future__ import annotations
from abc import ABC, abstractmethod
from ipywidgets import Button, HBox, ValueWidget


class Context(ValueWidget):
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    _state = None
    """
    A reference to the current state of the Context.
    """

    def __init__(self, state: State) -> None:
        self.transition_to(state)
        
        self.__next_button = Button(
            description="NEXT",
            button_style="info",
            icon="arrow-right"
        )
        self.__next_button.on_click(self.__on_click_next_button)
        
        self.__reset_button = Button(
            description="RESET",
            button_style="info",
            icon="power-off"
        )
        self.__next_button.on_click(self.__on_click_reset_button)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        # print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    The Context delegates part of its behavior to the current State object.
    """
    
    @property
    def hbox_buttons(self):
        return HBox([self.__reset_button, self.__next_button])
    
    @property
    def next_button(self):
        return self.__next_button
    
    @property
    def reset_button(self):
        return self.__reset_button
    
    def __on_click_next_button(self, btn):
        self._state.handle_next_button_click()
        
    def __on_click_reset_button(self, btn):
        self._state.handle_reset_button_click()
    
    
class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

@property
def context(self) -> Context:
    return self._context

@context.setter
def context(self, context: Context) -> None:
    self._context = context

@abstractmethod
def handle_next_button_click(self) -> None:
    pass

@abstractmethod
def handle_reset_button_click(self) -> None:
    pass