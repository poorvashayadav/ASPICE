package test.aspice;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MainTest {

    @Test
    void testExample() {
        assertTrue(true, "This test should pass.");
    }

    @Test
    void testIsEven() {
        assertTrue(Main.isEven(2), "2 should be even.");
    }
}
