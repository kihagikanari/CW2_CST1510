class ITTicket:
    """Represents an IT support ticket."""

    def __init__(self, ticket_id: int, assigned_to: str, created_at: str, resolution_time_hours: float, status: str, priority: str = "", description: str = ""):
        self.__id = ticket_id
        self.__assigned_to = assigned_to
        self.__resolution_time_hours = resolution_time_hours
        self.__status = status
        self.__priority = priority
        self.__description = description
        self.__created_at = created_at

    def get_id(self) -> int:
        return self.__id

    def get_assigned_to(self) -> str:
        return self.__assigned_to

    def get_created_at(self) -> str:
        return self.__created_at

    def get_resolution_time_hours(self) -> float:
        return self.__resolution_time_hours

    def get_status(self) -> str:
        return self.__status

    def get_priority(self) -> str:
        return self.__priority

    def get_description(self) -> str:
        return self.__description

    def close_ticket(self) -> None:
        self.__status = "Closed"

    def is_bottleneck(self, threshold: float = 48.0) -> bool:
        """Checking if ticket resolution time exceeds the threshold."""
        return self.__resolution_time_hours > threshold

    def __str__(self) -> str:
        return f"Ticket {self.__id}: {self.__assigned_to} - {self.__status}"