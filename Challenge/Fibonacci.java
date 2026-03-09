public class Fibonacci {
    public static long calculate(int n) {
        if (n <= 1) return n;
        
        long a = 0;
        long b = 1;
        
        for (int i = 2; i <= n; i++) {
            long sum = a + b;
            a = b;
            b = sum;
        }
        return b;
    }

    // Test Case
    public static void main(String[] args) {
        assert calculate(0) == 0;
        assert calculate(1) == 1;
        assert calculate(5) == 5;
        assert calculate(10) == 55;
        System.out.println("Fibonacci Tests Passed");
    }
}