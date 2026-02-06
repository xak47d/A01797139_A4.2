"""
Convert numbers to binary and hexadecimal representations.

This module provides manual conversion algorithms without using
built-in conversion functions.
"""

import sys
import time


def int_to_binary(n):
    """Convert an integer to its binary representation."""
    if n == 0:
        return "0"
    is_negative = n < 0
    n = abs(n)
    binary_digits = []
    while n > 0:
        remainder = n % 2
        binary_digits.append(str(remainder))
        n = n // 2
    binary_digits.reverse()
    result = ''.join(binary_digits)
    if is_negative:
        result = '-' + result
    return result


def int_to_hexadecimal(n):
    """Convert an integer to its hexadecimal representation."""
    hex_chars = "0123456789ABCDEF"
    if n == 0:
        return "0"
    is_negative = n < 0
    n = abs(n)
    hex_digits = []
    while n > 0:
        remainder = n % 16
        hex_digits.append(hex_chars[remainder])
        n = n // 16
    hex_digits.reverse()
    result = ''.join(hex_digits)
    if is_negative:
        result = '-' + result
    return result


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
                        num = int(float(line))
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


def write_results(filename, conversions, elapsed_time, items_info, errors):
    """Write conversion results to a file."""
    total_items = items_info['total']
    valid_items = items_info['valid']
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("=" * 60 + "\n")
            file.write("CONVERSION RESULTS\n")
            file.write("=" * 60 + "\n\n")
            file.write(f"Total items in file: {total_items}\n")
            file.write(f"Valid items: {valid_items}\n")
            file.write(f"Invalid items: {len(errors)}\n\n")
            file.write("-" * 60 + "\n")
            file.write("CONVERSIONS\n")
            file.write("-" * 60 + "\n\n")
            file.write(f"{'Decimal':<15} {'Binary':<25} {'Hexadecimal':<20}\n")
            file.write("-" * 60 + "\n")
            for num, binary, hex_val in conversions:
                file.write(f"{num:<15} {binary:<25} {hex_val:<20}\n")
            file.write("-" * 60 + "\n")
            file.write(f"\nElapsed time:       {elapsed_time:.6f} seconds\n")
            file.write("=" * 60 + "\n")
    except (IOError, OSError) as e:
        print(f"Error writing results: {e}")


def main():
    """Main function to convert numbers and display results."""
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py <file_with_data.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    output_filename = "ConvertionResults.txt"

    start_time = time.time()

    numbers, errors = read_numbers_from_file(filename)

    if not numbers:
        print("No valid numbers found in file.")
        sys.exit(1)

    conversions = []
    for num in numbers:
        binary = int_to_binary(num)
        hex_val = int_to_hexadecimal(num)
        conversions.append((num, binary, hex_val))

    elapsed_time = time.time() - start_time

    items_info = {
        'total': len(numbers) + len(errors),
        'valid': len(numbers)
    }

    print("\n" + "=" * 60)
    print("CONVERSION RESULTS")
    print("=" * 60)
    print(f"\nTotal items in file: {items_info['total']}")
    print(f"Valid items: {items_info['valid']}")
    print(f"Invalid items: {len(errors)}")
    print("\n" + "-" * 60)
    print("CONVERSIONS")
    print("-" * 60)
    print(f"\n{'Decimal':<15} {'Binary':<25} {'Hexadecimal':<20}")
    print("-" * 60)
    for num, binary, hex_val in conversions:
        print(f"{num:<15} {binary:<25} {hex_val:<20}")
    print("-" * 60)
    print(f"\nElapsed time:       {elapsed_time:.6f} seconds")
    print("=" * 60)

    write_results(
        output_filename, conversions, elapsed_time, items_info, errors
    )


if __name__ == "__main__":
    main()
