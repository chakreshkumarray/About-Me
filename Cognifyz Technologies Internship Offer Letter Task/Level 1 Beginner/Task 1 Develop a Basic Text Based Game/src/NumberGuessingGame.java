import java.util.Random;
import java.util.Scanner;

public class NumberGuessingGame {
    public static void main(String[] args){
      /*
      Game Rules and Logic
      The Number Guessing Game is a logic-based application that relies on conditional loops and state validation.

      1. Initialization: The system generates a random "target" integer within a defined range (1–100)
                         and sets a limit on attempts (5).

      2. The Loop:     The game enters a while loop that runs as long as the player has attempts remaining.

      3. Input & Validation: Inside the loop, the program accepts user input.
        i. Sanitization:   It ensures the input is a valid integer.
        ii. Range Check:   It validates that the number is within the playable range (ignoring negatives/zero).

      4. Comparison Logic: The player's guess is compared against the target,
        i. Equal:     The hasWon flag becomes true, and the loop breaks (Win).
        ii. Inequal:  The system uses else-if logic to provide directional feedback ("Too low" or "Too high")
                      and increments the attempt counter.

      5. Termination: The game ends when the loop breaks (Win) or the counter hits the limit (Loss),
                      displaying the final result.
      */

        // Setup Game Utilities
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        // Define Game rule and variables
        int lowerBound = 1;
        int upperBound = 100;
        int numberToGuess = random.nextInt(upperBound) + 1; // generate 1 to 100
        int maxAttempts = 5;
        int attemptsUsed = 0;
        boolean hasWon = false;

        System.out.println("### Welcome! to the number guessing ###");
        System.out.println("I have picked a number between " + lowerBound + " and " + upperBound + ".");
        System.out.println("You have " + maxAttempts + " attempts to guess it.\n");

        // Manage Game Flow (Loop & Conditionals)
        while (attemptsUsed < maxAttempts){
            System.out.print("Enter your Guess: ");

            // Validate if input is an Integer
            if (scanner.hasNextInt()){
                int playerGuess = scanner.nextInt();

                // Handle Negative and Zero
                if (playerGuess <= 0) {
                    System.out.println("Error: Input must be greater than 0. Please try again.\n");
                    continue; // Skip the rest of the loop, do not count attempt
                }

                attemptsUsed++; // Increment attempt only if input is valid

                // Conditional Statements
                if (playerGuess == numberToGuess){
                    hasWon = true;
                    break; // Exit the loop immediately on win
                } else if (playerGuess < numberToGuess) {
                    System.out.println("Too low! Try a higher number.");
                } else {
                    System.out.println("Too high! Try a lower number.");
                }

                System.out.println("Attempts remaining: "+(maxAttempts - attemptsUsed) + "\n");

            } else {
                // Handle invalid non-integer input (e.g., "abc")
                System.out.println("Invalid input! Please enter a valid number.\n");
                scanner.next(); // Clear the invalid input from scanner buffer
            }
        }

        // End Game Results
        System.out.println("--- Game Over ---");
        if (hasWon) {
            System.out.println("Congratulations! You guessed the number " + numberToGuess + " in "
                    + attemptsUsed + " attempts.");
        } else {
            System.out.println("You've run out of attempts. The number was: " + numberToGuess);
        }

        scanner.close();
    }
}