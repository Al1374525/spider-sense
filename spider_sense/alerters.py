class Alerter:
    
    def send(self, message):
        raise NotImplementedError("Subclasses must be implement send()")

    def status(self, message):
        raise NotImplementedError("Subclasses must implement status()")


class ConsoleAlerter(Alerter):
    
    def send(self, message):
        print(f"*** ALERT *** {message}")

    def status(self, message):
        print(f"[status] {message}")
