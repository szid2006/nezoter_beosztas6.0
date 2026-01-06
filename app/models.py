class Worker:
    def __init__(self, name, unavailable, preferred_shows, is_ek):
        self.name = name
        self.unavailable = unavailable  # list of (start, end)
        self.preferred_shows = preferred_shows
        self.is_ek = is_ek
        self.assign_count = 0
        self.role_history = []


class Shift:
    def __init__(self, show_name, datetime, required_roles):
        self.show_name = show_name
        self.datetime = datetime
        self.required_roles = required_roles
        self.assigned = {}
