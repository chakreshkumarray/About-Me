import java.util.List;
import java.util.Arrays;

public class VectorSum {
    // Using List<Long> to mimic vector<u64>
    public static long calculate(List<Long> numbers) {
        long sum = 0;
        for (long num : numbers) {
            sum += num;
        }
        return sum;
    }

    // Test Case
    public static void main(String[] args) {
        List<Long> vec1 = Arrays.asList(1L, 2L, 3L, 4L, 5L);
        assert calculate(vec1) == 15;

        List<Long> vec2 = Arrays.asList(10L, 20L, 30L);
        assert calculate(vec2) == 60;
        
        System.out.println("Vector Sum Tests Passed");
    }
} 
