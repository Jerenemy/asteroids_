class RenderLayer:
    def __init__(self, render_function, z_index, states=None, bools=None):
        """
        Represents a rendering layer.

        Args:
            render_function (callable): A function to render this layer.
            z_index (int): Determines the order of rendering (lower numbers render first).
            states (list, optional): A list of game states where this layer should render. Defaults to None (renders in all states).
        """
        self.render_function = render_function
        self.z_index = z_index
        self.states = states if states is not None else []
        self.bools = bools if bools else []

    def render(self, screen, game_state):
        """
        Call the render function for this layer if the state matches.

        Args:
            screen: The Pygame screen to render on.
            game_state (str): The current game state.
        """
        if (not self.states or game_state in self.states) and (not self.bools or all(self.bools)):
            self.render_function(screen)


class RenderManager:
    def __init__(self):
        self.layers = []

    def add_layer(self, render_function, z_index, states=None):
        """
        Add a render layer.

        Args:
            render_function (callable): The function to render this layer.
            z_index (int): Determines the rendering order.
            states (list, optional): A list of states where this layer renders. Defaults to None (renders in all states).
        """
        layer = RenderLayer(render_function, z_index, states)
        self.layers.append(layer)
        self.layers.sort(key=lambda l: l.z_index)  # Keep layers sorted by z-index

    def render(self, screen, game_state):
        """
        Render all layers in the correct order for the given state.

        Args:
            screen: The Pygame screen to render on.
            game_state (str): The current game state.
        """
        for layer in self.layers:
            layer.render(screen, game_state)