####################
###  DEFINITION  ###
####################

# Define our function that takes a string representing a password and returns a bool
def is_valid(password: str) -> bool:
    # Docstrings are just good practice
    '''Check validity of a password as suggested by a new user when registering'''
    # Define a "constant" (not really) of special characters
    SPECIAL_CHARS = ("!", "?", "&", "%", "*", "@")
    # Create a set of constraints, this is coming straight from our requirements
    # Each of these constraints is an expression that resolves to a boolean
    # Note: calling set() explicitly is not strictly required, but it prevents confusion
    # because curly braces are much more commonly used to define dicts
    constraints = set({
        # Length must be at least 6; len(password) > 5 also works but is less explicit
        len(password) >= 6,
        # At least one character must be uppercase
        any(character.isupper() for character in password),
        # At least one character must be lowercase
        any(character.islower() for character in password),
        # At least one character must be numeric
        any(character.isnumeric() for character in password),
        # At least one of the special characters defined earlier must appear
        any(special_char in password for special_char in SPECIAL_CHARS),
    })
    # If all constraints resolve to True, return True; if not, return False
    return all(constraints)


###############
###  USAGE  ###
###############

# Assume that part of the main program flow imports the above function definition
# Input validation is taken care of by another bit of logic, so we don't have to worry
# At this point in the main flow we have a variable called 'user_password'; for the purposes
# of this example we will assign it manually.
user_password = "PythonR0cks!"

if is_valid(user_password):
    # Continue the normal flow
    print(f"Password {user_password} is valid. Thank you for joining!")
else:
    # Tell the user to try again
    print(f"Password {user_password} is not valid. Please try again.")
