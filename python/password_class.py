####################
###  DEFINITION  ###
####################

# Create our Password class that extends the str type
class Password(str):
    # Docstrings are awesome
    '''Check the validity of passwords provided by a new user when registering'''

    # Define a "private" (not really) "constant" (not really) tuple of special chars
    _SPECIAL_CHARS = ("!", "?", "&", "%", "*", "@")

    # Define a "private" (not really) method that returns a set of constraints
    # This cannot be a field, because the class wants to resolve the expressions when a
    # class instance is created - which is not possible if it's a field.
    def _constraints(self) -> set:
        # Explicit set
        return set({
            # All of these are identical to the function definition and self-explanatory
            len(self) >= 6,
            any(character.islower() for character in self),
            any(character.isupper() for character in self),
            any(character.isnumeric() for character in self),
            any(special_char in self for special_char in Password._SPECIAL_CHARS),
            })

    @property
    def is_valid(self) -> bool:
        return all(self._constraints())


###############
###  USAGE  ###
###############

# Assume that part of the main program flow imports the above function definition
# Input validation is taken care of by another bit of logic, so we don't have to worry
# At this point in the main flow we have a variable called 'user_password'; for the purposes
# of this example we will assign it manually.
user_password = Password("PythonR0cks!")

if user_password.is_valid:
    # Continue the normal flow
    print(f"Password {user_password} is valid. Thank you for joining!")
else:
    # Tell the user to try again
    print(f"Password {user_password} is not valid. Please try again.")
