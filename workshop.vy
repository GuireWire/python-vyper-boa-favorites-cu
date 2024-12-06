# I'm a comment!

# pragma version 0.4.0
# @license MIT

struct Person:
    set_bool: bool
    name: String[100]

my_bool: public(bool)

# Static Array/List
list_of_bools_set: public(bool[5])
list_of_people: public(Person[5])
list_of_people_index: uint256

name_to_set_bool: HashMap[String[100], bool]

@deploy
def __init__():
    self.my_bool = True

@external
def set_bool(new_bool: bool):
    self.my_bool = new_bool

@external
@view
def get_bool() -> bool:
    return self.my_bool

@external
def add_person(name: String[100], set_bool: bool):
    new_person: Person = Person(set_bool = set_bool, name = name)
    self.list_of_people[self.list_of_people_index] = new_person
    self.list_of_bools_set[self.list_of_people_index] = set_bool
    self.list_of_people_index += 1
    self.name_to_set_bool[name] = set_bool