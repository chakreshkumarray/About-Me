public class PrimeChecker {
    public static boolean isPrime(long n) {
        if (n <= 1) return false;
        
        // We only check up to the square root of n
        for (long i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }

    // Test Case
    public static void main(String[] args) {
        assert isPrime(2) == true;
        assert isPrime(17) == true;
        assert isPrime(4) == false;
        assert isPrime(100) == false;
        System.out.println("Prime Tests Passed");
    }
}