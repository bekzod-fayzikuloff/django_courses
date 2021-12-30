class BaseActionMixin:
    serializer_class = None
    actions = dict()

    def get_serializer_action(self, action: str):
        if action is None:
            return self.serializer_class
        return self.actions.get(action, self.serializer_class)
