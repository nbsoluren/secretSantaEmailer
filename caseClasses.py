from dataclasses import dataclass

@dataclass
class Participant:
  name: str
  email: str

@dataclass
class Assignment:
  santa: Participant
  child: Participant
