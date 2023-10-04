public class Main {
    public static void main(String[] args) {
        Password user_password = new Password("JavaR0cks!");

        if (user_password.isValid()) {
            System.out.println("Password " + user_password + " is valid!");
        } else {
            System.out.println("Password " + user_password + " is not valid.");
        }
    }
}
