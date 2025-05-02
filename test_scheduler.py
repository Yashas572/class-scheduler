from pyswip import Prolog
import tempfile
import os

# Fixed Prolog KB as a string
kb = """
class(cs101).
class(cs102).
class(math201).
class(phy101).

room(roomA).
room(roomB).
room(roomC).

needs_time(cs101, monday10am).
needs_time(cs102, monday10am).
needs_time(math201, tuesday1pm).
needs_time(phy101, monday10am).

needs_equipment(cs101, projector).
needs_equipment(cs102, whiteboard).
needs_equipment(math201, projector).
needs_equipment(phy101, lab).

has(roomA, monday10am).
has(roomB, monday10am).
has(roomC, monday10am).
has(roomA, tuesday1pm).

has(roomA, projector).
has(roomB, whiteboard).
has(roomC, lab).

can_schedule(Class, Room) :-
    needs_time(Class, Time),
    needs_equipment(Class, Equipment),
    has(Room, Time),
    has(Room, Equipment).
"""

# Save KB to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".pl", mode="w") as temp_file:
    temp_file.write(kb)
    filename = temp_file.name.replace(os.sep, '/')

# Load into Prolog
prolog = Prolog()
list(prolog.query(f"consult('{filename}')"))

# Run test queries
tests = [
    ("cs101", "roomA"),
    ("cs102", "roomA"),
    ("cs102", "roomB"),
    ("phy101", "roomC"),
    ("math201", "roomC")
]

print("Test Results:")
for cls, room in tests:
    result = list(prolog.query(f"can_schedule({cls}, {room})"))
    print(f"can_schedule({cls}, {room}) ->", "true" if result else "false")

# Clean up
os.remove(filename)

