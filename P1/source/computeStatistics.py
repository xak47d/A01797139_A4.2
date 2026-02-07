"""
Compute descriptive statistics from a file containing numbers.

This module calculates mean, median, mode, variance, and standard
deviation using basic algorithms without external libraries.
"""

import sys
import time


def calculate_mean(numbers):
    """Calculate the arithmetic mean of a list of numbers."""
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)


def manual_sort(numbers):
    """Sort a list of numbers using bubble sort algorithm."""
    result = numbers.copy()
    n = len(result)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


def calculate_median(numbers):
    """Calculate the median of a list of numbers."""
    sorted_numbers = manual_sort(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    return sorted_numbers[mid]


def calculate_mode(numbers):
    """Calculate the mode(s) and their frequency."""
    frequency = {}
    for num in numbers:
        if num in frequency:
            frequency[num] = frequency[num] + 1
        else:
            frequency[num] = 1
    max_freq = 0
    modes = []
    for num, freq in frequency.items():
        if freq > max_freq:
            max_freq = freq
            modes = [num]
        elif freq == max_freq:
            modes.append(num)
    return modes, max_freq


def calculate_sqrt(n):
    """Calculate square root using Newton's method."""
    if n == 0:
        return 0
    x = n
    epsilon = 0.000001
    while True:
        root = (x + n / x) / 2
        if abs(root - x) < epsilon:
            return root
        x = root


def calculate_variance(numbers, mean):
    """Calculate the population variance of a list of numbers."""
    total = 0
    for num in numbers:
        diff = num - mean
        total = total + (diff * diff)
    return total / len(numbers)


def calculate_std_dev(variance):
    """Calculate the population standard deviation."""
    return calculate_sqrt(variance)


def read_numbers_from_file(filename):
    """Read numbers from a file, handling invalid data gracefully."""
    numbers = []
    errors = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line:
                    try:
                        num = float(line)
                        numbers.append(num)
                    except ValueError:
                        error_msg = f"Line {line_num}: Invalid data '{line}'"
                        errors.append(error_msg)
                        print(error_msg)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    return numbers, errors


def write_results(filename, stats, elapsed_time, items_info, errors):
    """Write statistics results to a file."""
    total_items = items_info['total']
    valid_items = items_info['valid']
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("=" * 50 + "\n")
            file.write("STATISTICS RESULTS\n")
            file.write("=" * 50 + "\n\n")
            file.write(f"Total items in file: {total_items}\n")
            file.write(f"Valid items: {valid_items}\n")
            file.write(f"Invalid items: {len(errors)}\n\n")
            file.write("-" * 50 + "\n")
            file.write("DESCRIPTIVE STATISTICS\n")
            file.write("-" * 50 + "\n\n")
            file.write(f"Mean:               {stats['mean']:.6f}\n")
            file.write(f"Median:             {stats['median']:.6f}\n")
            if len(stats['mode']) == 1:
                file.write(f"Mode:               {stats['mode'][0]}\n")
            else:
                file.write(f"Mode:               {stats['mode']}\n")
            file.write(f"Mode Frequency:     {stats['mode_freq']}\n")
            file.write(f"Variance:           {stats['variance']:.6f}\n")
            file.write(f"Std Deviation:      {stats['std_dev']:.6f}\n")
            file.write("\n" + "-" * 50 + "\n")
            file.write(f"Elapsed time:       {elapsed_time:.6f} seconds\n")
            file.write("=" * 50 + "\n")
    except (IOError, OSError) as e:
        print(f"Error writing results: {e}")


def main():
    """Main function to compute and display statistics."""
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py <file_with_data.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    output_filename = "StatisticsResults.txt"

    start_time = time.time()

    numbers, errors = read_numbers_from_file(filename)

    if not numbers:
        print("No valid numbers found in file.")
        sys.exit(1)

    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    modes, mode_freq = calculate_mode(numbers)
    variance = calculate_variance(numbers, mean)
    std_dev = calculate_std_dev(variance)

    elapsed_time = time.time() - start_time

    stats = {
        'mean': mean,
        'median': median,
        'mode': modes,
        'mode_freq': mode_freq,
        'variance': variance,
        'std_dev': std_dev
    }

    items_info = {
        'total': len(numbers) + len(errors),
        'valid': len(numbers)
    }

    print("\n" + "=" * 50)
    print("STATISTICS RESULTS")
    print("=" * 50)
    print(f"\nTotal items in file: {items_info['total']}")
    print(f"Valid items: {items_info['valid']}")
    print(f"Invalid items: {len(errors)}")
    print("\n" + "-" * 50)
    print("DESCRIPTIVE STATISTICS")
    print("-" * 50)
    print(f"\nMean:               {mean:.6f}")
    print(f"Median:             {median:.6f}")
    if len(modes) == 1:
        print(f"Mode:               {modes[0]}")
    else:
        print(f"Mode:               {modes}")
    print(f"Mode Frequency:     {mode_freq}")
    print(f"Variance:           {variance:.6f}")
    print(f"Std Deviation:      {std_dev:.6f}")
    print("\n" + "-" * 50)
    print(f"Elapsed time:       {elapsed_time:.6f} seconds")
    print("=" * 50)

    write_results(output_filename, stats, elapsed_time, items_info, errors)


if __name__ == "__main__":
    main()
