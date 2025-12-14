class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(self, incident_id: int, category: str, severity: str,
                 status: str, description: str, timestamp: int = ""):
        self.__id = incident_id
        self.__category = category
        self.__severity = severity
        self.__status = status
        self.__description = description
        self.__timestamp = timestamp

    def get_id(self) -> int:
        return self.__id

    def get_category(self) -> str:
        return self.__category

    def get_severity(self) -> str:
        return self.__severity

    def get_status(self) -> str:
        return self.__status

    def get_description(self) -> str:
        return self.__description

    def get_timestamp(self) -> int:
        return self.__timestamp

    def update_status(self, new_status: str) -> None:
        self.__status = new_status

    def is_critical(self) -> bool:
        """checking if incident is critical or high severity."""
        return self.__severity.lower() in ['critical', 'high']

    def get_severity_level(self) -> int:
        """returning an integer severity level."""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)

    def __str__(self) -> str:
        return f"Incident {self.__id} [{self.__severity.upper()}] {self.__category}"