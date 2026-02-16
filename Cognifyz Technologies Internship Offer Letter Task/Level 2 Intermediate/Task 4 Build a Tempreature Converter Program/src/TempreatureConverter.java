import java.util.InputMismatchException;
import java.util.Scanner;

public class TempreatureConverter {
    public static void main(String[] args) {

        // use 'try-with-resources' to automatically close the scanner (Bonus points for this!)
        // Step 1: Get user choice
        // Step 2: Handle Exit logic first
        // Step 3: Validate menu range
        // Step 4: Get temperature input
        // Step 5: Perform Conversion
        try (Scanner scanner = new Scanner(System.in)) {

            while (true) {
                System.out.println("\n=== Temperature Converter ===");
                System.out.println("1. Fahrenheit to Celsius");
                System.out.println("2. Celsius to Fahrenheit");
                System.out.println("3. Exit");
                System.out.print("Choose an option: ");

                try {
                    int choice = scanner.nextInt();
                    if (choice == 3) {
                        System.out.println("Exiting program. Goodbye!");
                        break;
                    }
                    if (choice != 1 && choice != 2) {
                        System.out.println("Error: Please select 1, 2, or 3.");
                        continue;
                    }
                    System.out.print("Enter temperature value: ");
                    double temp = scanner.nextDouble();

                    if (choice == 1) {
                        double result = (temp - 32) * 5 / 9;
                        System.out.printf("Result: %.2f Fahrenheit = %.2f Celsius%n", temp, result);
                    } else {
                        double result = (temp * 9 / 5) + 32;
                        System.out.printf("Result: %.2f Celsius = %.2f Fahrenheit%n", temp, result);
                    }

                } catch (InputMismatchException e) {
                    System.out.println("Error: Invalid input! Please enter a valid number.");
                    scanner.nextLine();
                }
            }
        }

    }
}