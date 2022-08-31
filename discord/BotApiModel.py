class BotApiModel:
    def __init__(self):
        self.Id = None
        self.Name = None
        self.Description = None
        self.IsRunning = False

    def serialize(self):
        dict = {}
        for attr in vars(self):
            attr_value = getattr(self, attr)
            dict[attr] = attr_value
        return dict
