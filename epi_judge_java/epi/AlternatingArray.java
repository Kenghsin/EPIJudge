package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;
import epi.test_framework.TestFailure;
import epi.test_framework.TestUtils;
import epi.test_framework.TimedExecutor;

import java.util.List;

public class AlternatingArray {
  public static void rearrange(List<Integer> A) {
    // Implement this placeholder.
    return;
  }

  private static void checkOrder(List<Integer> A) throws TestFailure {
    for (int i = 0; i < A.size(); ++i) {
      if ((i % 2) != 0) {
        if (A.get(i) < A.get(i - 1)) {
          throw new TestFailure()
              .withProperty(TestFailure.PropertyName.RESULT, A)
              .withMismatchInfo(
                  i, "A[i - 1] <= A[i]",
                  String.format("%d > %d", A.get(i - 1), A.get(i)));
        }
        if (i < A.size() - 1) {
          if (A.get(i) < A.get(i + 1)) {
            throw new TestFailure()
                .withProperty(TestFailure.PropertyName.RESULT, A)
                .withMismatchInfo(
                    i, "A[i] >= A[i + 1]",
                    String.format("%d < %d", A.get(i), A.get(i + 1)));
          }
        }
      } else {
        if (i > 0) {
          if (A.get(i - 1) < A.get(i)) {
            throw new TestFailure()
                .withProperty(TestFailure.PropertyName.RESULT, A)
                .withMismatchInfo(
                    i, "A[i - 1] >= A[i]",
                    String.format("%d < %d", A.get(i - 1), A.get(i)));
          }
        }
        if (i < A.size() - 1) {
          if (A.get(i + 1) < A.get(i)) {
            throw new TestFailure()
                .withProperty(TestFailure.PropertyName.RESULT, A)
                .withMismatchInfo(
                    i, "A[i] <= A[i + 1]",
                    String.format("%d > %d", A.get(i), A.get(i + 1)));
          }
        }
      }
    }
  }

  @EpiTest(testfile = "alternating_array.tsv")
  public static void rearrangeWrapper(TimedExecutor executor, List<Integer> A)
      throws Exception {
    List<Integer> result = new ArrayList<>(A);
    executor.run(() -> rearrange(result));

    TestUtils.assertAllValuesPresent(A, result);
    checkOrder(result);
  }

  public static void main(String[] args) {
    // The timeout is set to 15 seconds for each test case.
    // If your program ends with TIMEOUT error, and you want to try longer time
    // limit, you can extend the limit by changing the following line.
    long timeoutSeconds = 15;

    System.exit(
        GenericTest
            .runFromAnnotations(args, timeoutSeconds,
                                new Object() {}.getClass().getEnclosingClass())
            .ordinal());
  }
}
