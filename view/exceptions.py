class IncorrectActionType(Exception):
    def __init__(self, item_type: type):
        message = f"Item type {item_type} can't be used as an action function!"
        super().__init__(message)
