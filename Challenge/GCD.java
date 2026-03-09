public class GCD {
    public static long calculate(long a, long b) {
        while (b != 0) {
            long temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    // Test Case
    public static void main(String[] args) {
        assert calculate(48, 18) == 6;
        assert calculate(100, 50) == 50;
        assert calculate(17, 19) == 1;
        System.out.println("GCD Tests Passed");
    }
}