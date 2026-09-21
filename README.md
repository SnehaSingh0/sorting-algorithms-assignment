# Sorting Algorithms – Assignment 1

## Original Question

Implement 5 favourite sorting algorithms. Compare the time taken by each algorithm on generated student records.

- Each student record should be at least 4 KB.
- Test with 10K, 100K and 100L records.
- Compare the execution time of the algorithms.

## Initial Finding

Using approximately 4 KB per record would require approximately 40 GB for 100L records, which was not practical for main-memory sorting on the available system.

## Modified Approach

After discussion with the mentor:

- Record size changed from approximately 4 KB to approximately 40 bytes.
- Sorting remained main-memory based.
- Dataset sizes were increased gradually to identify the practical range.
- A **30-minute execution limit** was used for each algorithm.
- Algorithms exceeding the limit were recorded as `TIMEOUT`.

## Sorting Algorithms

| Algorithm | Time Complexity |
|---|---|
| Bubble Sort | O(n²) |
| Selection Sort | O(n²) |
| Insertion Sort | O(n²) worst case |
| Merge Sort | O(n log n) |
| Quick Sort | O(n log n) average |

The five algorithms provide a comparison between three O(n²) algorithms and two generally faster O(n log n) algorithms.

## Performance Results

| Records | Bubble Sort | Selection Sort | Insertion Sort | Merge Sort | Quick Sort |
|---:|---:|---:|---:|---:|---:|
| 10K | 14.053327 s | 12.295507 s | 4.168541 s | 0.040462 s | 0.030228 s |
| 20K | 56.248850 s | 46.763717 s | 17.099703 s | 0.085765 s | 0.059127 s |
| 30K | 134.237999 s | 109.977308 s | 40.230519 s | 0.138444 s | 0.094763 s |
| 40K | 231.200777 s | 193.640661 s | 76.887638 s | 0.198937 s | 0.129004 s |
| 50K | TIMEOUT | TIMEOUT | 115.736298 s | 0.242417 s | 0.161153 s |
| 100K | TIMEOUT | TIMEOUT | TIMEOUT | 1.107112 s | 0.760883 s |

**TIMEOUT:** Algorithm did not finish within the 30-minute limit.

## Findings

- Bubble Sort and Selection Sort became impractical as the dataset size increased.
- Insertion Sort completed 50K but timed out at 100K.
- Merge Sort and Quick Sort completed 100K within the time limit.
- The performance difference between O(n²) and O(n log n) algorithms became much more noticeable with larger datasets.
- 40K was the highest tested size completed by Bubble Sort and Selection Sort within the 30-minute limit.

## Key Learnings

- Implementing the algorithms helped understand their practical behaviour beyond theory.
- Increasing the number of records had a much larger effect on the O(n²) algorithms.
- Record size can become a major memory constraint for large datasets.
- Testing progressively larger datasets helped identify the practical range of each algorithm.
- A time limit is useful when an algorithm becomes impractical to run indefinitely.
- Sorting correctness needs to be checked along with execution time.

## Execution & Results

- **Language:** Python
- **Execution timer:** `time.perf_counter()`
- **Execution limit:** 30 minutes per algorithm
- Each completed result was checked for correct sorting.
- After each benchmark run, the program automatically generated a CSV result file.
- The CSV contains:
  - Dataset size
  - Algorithm
  - Execution time
  - Status (`PASS` / `TIMEOUT`)

Example CSV output:

```text
dataset size,algorithm,execution time,status
10000,Bubble Sort,14.053327,PASS
10000,Selection Sort,12.295507,PASS
10000,Insertion Sort,4.168541,PASS
10000,Merge Sort,0.040462,PASS
10000,Quick Sort,0.030228,PASS