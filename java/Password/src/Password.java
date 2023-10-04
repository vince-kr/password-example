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
