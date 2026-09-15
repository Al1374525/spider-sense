class Alerter:
    
    def send(self, message):
        raise NotImplementedError("Subclasses must be implement send()")


class ConsoleAlerter(Alerter):
    
    def send(self, message):
        print(f"*** ALERT *** {message}")