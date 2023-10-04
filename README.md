# Java through Python: validating a password

Let's write some simple logic to validate a password, such as may be used as part of registering new users on a website.

We'll start with using a Python *function*, implement the same logic in a Python *class*, and finally translate that to Java.

## Outline & requirements

For this small example I don't want to make things more complicated than they need to be, so we make some assumptions about things that happen before and after the usage examples:

1. An actor is creating a new user account on a popular social media platform. As part of this process, they need to set a password for their new account.
2. The actor enters their proposed password and clicks "Create my account".
3. The platform's application backend checks (among other things) that the password meets the requirements for a valid password.
4. The application presents a new page to the actor.
    - If their password is valid the actor will see "Password xxx is valid. Thank you for joining!"
    - If their password is not valid the actor will see "Password xxx is not valid. Please try again."

In order to make this simple example work, I will simply assign a string litral to a variable called `user_password` and pretend that it came from the application frontend.

The Python files - validate_password_function.py and password_class.py - contain an *implementation* of the logic and, directly below it, an example of how this logic would be *used*. In an actual system the implementation and the usage would be split, with the function or class which implements the logic used somewhere far away from where it's defined.

The Java project will contain two classes, one per file: Main (in Main.java) and Password (in Password.java), with Main *using* the logic that is *implemented* in Password.

For either language, the requirements are summarised as follows:  
***Define some logic that takes in a user's intended password as a string, and returns a boolean to indicate whether the password is valid.***

A password is considered valid if it meets the following requirements:

- It is at least 6 characters long
- It contains at least one lowercase letter, one uppercase letter, and one number
- It contains at least one of the following special characters: !, ?, &, %, \*, @

## A Python function

### Defining the function

```python
def is_valid(password: str) -> bool:
    '''Check validity of a password as suggested by a new user when registering'''
    SPECIAL_CHARS = ("!", "?", "&", "%", "*", "@")
    constraints = set({
        len(password) >= 6,
        any(character.islower() for character in password),
        any(character.isupper() for character in password),
        any(character.isnumeric() for character in password),
        any(special_char in password for special_char in SPECIAL_CHARS),
    })
    return all(constraints)
```

Implementing this logic in Python is very straightforward. We define a function that takes a string and returns a boolean. We include a docstring to impress our boss.

First, we define a "constant" (not really, cos it's Python) tuple of the special characters. At least one of these should appear in the user's proposed password.

Next, we create a set of constraints. Note that explicitly calling `set()` here is not technically required; you could just use the curly brace notation. However:

1. Dictionary literals are created using curly braces, just like sets
2. Dictionaries are much more common than sets
3. A dictionary would also be a valid choice for this purpose

So in order to make my *intentions* as obvious as possible, I choose to use an explicit call to `set()` when creating my collection of constraints.

Each constraint is an expression that resolves to a boolean at runtime. Each of them is a clear representation of one of the constraints listed in our requirements.

Finally, we return the result of calling `all()` with our list of constraints. This will return `True` if all constraints are true or `False` otherwise.

### Using the function

```python
user_password = "PythonR0cks!"

if is_valid(user_password):
    # Much complicated logic that returns a page to welcome the actor
    print(f"Password {user_password} is valid. Thank you for joining!")
else:
    # Much complicated logic that returns a page to ask the actor to try again
    print(f"Password {user_password} is not valid. Please try again.")
```

### This approach

There are issues with this approach both in *definition* and in *usage*.

At definition, we create two data fields: one with a name (our tuple of special characters) and one anonymous (our set of constraints). There is nothing inherently wrong with defining local variables in a function body, but in this particular case these local variables represent a part of our *business rules*. It would be better if we could define both of these fields outside of the logic of the function.

At usage, the only thing I don't like is the somewhat clunky looking `if is_valid(user_password`. It reads fine, but being able to say `if user_password.is_valid` would be better.

These issues can be partly resolved by using a class. This also leads us to the real point of this exercise: extending built-in classes.

## A Python class

### Defining the class

```python
class Password(str):
    '''Check the validity of passwords provided by a new user when registering'''
    _SPECIAL_CHARS = ("!", "?", "&", "%", "*", "@")

    def _constraints(self) -> set:
        return set({
            len(self) >= 6,
            any(character.islower() for character in self),
            any(character.isupper() for character in self),
            any(character.isnumeric() for character in self),
            any(special_char in self for special_char in Password._SPECIAL_CHARS),
            })

    @property
    def is_valid(self) -> bool:
        return all(self._constraints())
```

This class works in a very similar way as the function defined earlier. The special chars are now a "private" (not really) "constant" (not really) class variable tuple. It would have been nice to store the constraints as a field as well, but I couldn't find a nice way to do so. Python tries to resolve the boolean expressions at runtime, so something like `len(password) >= 6` needs a valid field `password` to refer to - and this doesn't exist yet if we're just defining (as opposed to instantiating) the class.

It's possible to use a set of lambdas in a class variable and change the `is_valid` property accordingly:

```python
class Password(str):
    '''Check the validity of passwords provided by a new user when registering'''
    _CONSTRAINTS = set({
        lambda pw: len(pw) >= 6,
        lambda pw: any(character.islower() for character in pw),
        lambda pw: any(character.isupper() for character in pw),
        lambda pw: any(character.isnumeric() for character in pw),
        lambda pw: any(special_char in pw for special_char in Password._SPECIAL_CHARS),
    })

    _SPECIAL_CHARS = ("!", "?", "&", "%", "*", "@")

    @property
    def is_valid(self) -> bool:
        return all(constraint(self) for constraint in Password._CONSTRAINTS)
```

This indicates the reality that constraints are an attribute of the class as opposed to its instances - on the other hand, the *resolution* of the constraints (i.e. a value of True or False as opposed to the expression itself) is an attribute of an instance, so really there's an argument to be made for either choice. It's a matter of personal preference.  
The only way I could think of to define constraints as class fields rather than instance fields was by using functions (either several named functions, or a set of lambdas as above) and neither is as obvious as the first class definition.

Since we're extending `str`, our methods remain very concise and readable. Each boolean expression in the `_constraints()` method references self, indicating that each expression depends on an object of the class. Both this method and the `is_valid()` method take `self` as their only argument.

Extending built-in classes is a great way to use existing functionality that's often already very close to the behaviour that you need.

### Using the class

```python
user_password = Password("PythonR0cks!")

if user_password.is_valid:
    # Much complicated logic that returns a page to welcome the actor
    print(f"Password {user_password} is valid. Thank you for joining!")
else:
    # Much complicated logic that returns a page to ask the actor to try again
    print(f"Password {user_password} is not valid. Please try again.")
```

### This approach

The usage looks cleaner compared to the function version. Furthermore, since our `Password` class extends `str`, we can treat it as a string when printing to stdout - we don't need to implement a `__str__()` or `__repr__()` method manually!

## A Java class

### Defining the class

```java
class Password {

    private static final String SPECIAL_CHARS = "!?&%*@";

    private final String userPassword;

    public Password(String userPassword) {
        this.userPassword = userPassword;
    }

    private boolean[] constraints() {
        return new boolean[] {
                userPassword.length() >= 6,
                userPassword.matches(".*[a-z].*"),
                userPassword.matches(".*[A-Z].*"),
                userPassword.matches(".*[0-9].*"),
                userPassword.chars().anyMatch(ch -> SPECIAL_CHARS.indexOf(ch) >= 0)
        };
    }

    public boolean isValid() {
        for (boolean constraint : constraints()) {
            if (!constraint) {
                return false;
            }
        }
        return true;
    }

    @Override
    public String toString() {
        return userPassword;
    }
}
```

While writing this exercise, I learned that it is not possible to extend the `String` class. I'm not sure what the thinking is, but it makes for some interesting differences in *usage* between the Python and Java versions. For example, unlike Python, we need to define a `toString()` method that returns our password - if we tried to print our class without defining `toString()` it would simply print the memory address.

The `SPECIAL_CHARS` field is now properly private and readonly (`final`), and `userPassword` is similarly encapsulated. The constraints are still captured inside a method, because of the same reason as in Python: if they were an instance *variable*, then Java would want to resolve the boolean expressions at runtime, which is not possible as long as a class instance does not exist. I decided to use an array of boolean expressions because working with sets was unnecessarily complicated.

Java doesn't appear to have an equivalent to Python's `all()` built-in, so the `isValid()` method manually iterates over the constraints. It returns `false` on the first constraint that evaluates false, or true if it iterates over the whole collection without finding any `false`s.


### Using the class

```java
public class Main {
    public static void main(String[] args) {
        Password user_password = new Password("JavaR0cks!");

        if (user_password.isValid()) {
            System.out.println("Password " + user_password + " is valid. Thank you for joining!");
        } else {
            System.out.println("Password " + user_password + " is not valid. Please try again.");
        }
    }
}
```

### This approach

I find the usage to be a little bit less readable than Python's - Java needs a few more characters like parens around if-statements and of course curly braces, and I don't like that I need to call `isValid()` as a method instead of referencing it as a property (something that for example C# does support). I suppose this is just something to get used to.

## I hope this was useful!
