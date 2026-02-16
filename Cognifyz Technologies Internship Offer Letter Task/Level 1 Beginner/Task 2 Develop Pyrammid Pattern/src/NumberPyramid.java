import java.util.Scanner;

public class NumberPyramid {
    public static void main(String[] args) {

        /*
        Step 1: Select a Number Pattern
        We will generate a Center-Aligned Number Pyramid.
        Target Output (for height = 5):
        */
        Scanner input = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int num = input.nextInt();

        for (int i = 1; i <= num; i++){
            for (int space = 1; space <= (num -  i); space++){
                System.out.print(" ");
            }
            for (int j = 1; j <= i; j++){
                System.out.print(i+" ");
            }
            System.out.println();
        }
       /*
        Step 2 & 3: Develop Program & Control Structure
        To achieve this, we need Nested Loops:
        Outer Loop: Controls the number of rows (height).
        Inner Loop 1: Controls the spaces needed to push the numbers to the center.
        Inner Loop 2: Controls the printing of the actual numbers.

        Step 4: Verify Correctness (Dry Run)
        To verify the pattern without running the computer, we perform a "dry run" for a smaller number,
        like n = 3.

        Logic Trace:
        Row 1 (i = 1):
        Spaces: Loop runs (3 - 1) = 2 times. Output: [Space][Space]
        Numbers: Loop runs 1 time. Output: 1
        Result:  1 (Correct)
        Row 2 (i = 2):
        Spaces: Loop runs (3 - 2) = 1 time. Output: [Space]
        Numbers: Loop runs 2 times. Output: 2 2
        Result: 2 2 (Correct)
        Row 3 (i = 3):
        Spaces: Loop runs (3 - 3) = 0 times. Output: (No spaces)
        Numbers: Loop runs 3 times. Output: 3 3 3
        Result: 3 3 3  (Correct)
        The logic holds up. As i increases, the spaces decrease, and the count of numbers printed increases.
         */

    }
}