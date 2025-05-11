from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Process(Base):
    """Represents a process in the task manager.

    Attributes
    ----------
    id : int
        The unique identifier for the process.
    name : str
        The name of the process.
    status : str
        The current status of the process.
    start_time : str
        The start time of the process.
    end_time : str
        The end time of the process.
    duration : int
    status = Column(Enum(StatusEnum), index=True)
    error_message : str
        Any error message associated with the process.

    """

    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, index=True)
    start_time = Column(String, index=True)
    end_time = Column(String, index=True)
    duration = Column(Integer, index=True)
    error_message = Column(String, index=True)

    def __repr__(self):
        """Return a string representation of the process."""
        return f"<Process(name={self.name}, status={self.status})>"
