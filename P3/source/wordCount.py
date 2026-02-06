"""
Count word frequencies in a text file.

This module identifies distinct words and calculates their frequencies
using basic algorithms without external libraries.
"""

import sys
import time


def read_words_from_file(filename):
    """Read words from a file, handling errors gracefully."""
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    for part in parts:
                        clean_word = part.strip()
                        if clean_word:
                            words.append(clean_word)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    return words


def count_word_frequencies(words):
    """Count the frequency of each word in the list."""
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] = frequency[word] + 1
        else:
            frequency[word] = 1
    return frequency


def sort_by_frequency(frequency_dict):
    """Sort words by frequency in descending order."""
    items = list(frequency_dict.items())
    n = len(items)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if items[j][1] < items[j + 1][1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items


def write_results(filename, sorted_words, elapsed_time, total_words):
    """Write word count results to a file."""
    distinct_words = len(sorted_words)
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("=" * 60 + "\n")
            file.write("WORD COUNT RESULTS\n")
            file.write("=" * 60 + "\n\n")
            file.write(f"Total words: {total_words}\n")
            file.write(f"Distinct words: {distinct_words}\n\n")
            file.write("-" * 60 + "\n")
            file.write("WORD FREQUENCIES\n")
            file.write("-" * 60 + "\n\n")
            file.write(f"{'Word':<30} {'Frequency':<15}\n")
            file.write("-" * 60 + "\n")
            for word, count in sorted_words:
                file.write(f"{word:<30} {count:<15}\n")
            file.write("-" * 60 + "\n")
            file.write(f"\nElapsed time:       {elapsed_time:.6f} seconds\n")
            file.write("=" * 60 + "\n")
    except (IOError, OSError) as e:
        print(f"Error writing results: {e}")


def main():
    """Main function to count words and display results."""
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py <file_with_data.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    output_filename = "WordCountResults.txt"

    start_time = time.time()

    words = read_words_from_file(filename)

    if not words:
        print("No words found in file.")
        sys.exit(1)

    frequency = count_word_frequencies(words)
    sorted_words = sort_by_frequency(frequency)

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 60)
    print("WORD COUNT RESULTS")
    print("=" * 60)
    print(f"\nTotal words: {len(words)}")
    print(f"Distinct words: {len(sorted_words)}")
    print("\n" + "-" * 60)
    print("WORD FREQUENCIES")
    print("-" * 60)
    print(f"\n{'Word':<30} {'Frequency':<15}")
    print("-" * 60)
    for word, count in sorted_words:
        print(f"{word:<30} {count:<15}")
    print("-" * 60)
    print(f"\nElapsed time:       {elapsed_time:.6f} seconds")
    print("=" * 60)

    write_results(output_filename, sorted_words, elapsed_time, len(words))


if __name__ == "__main__":
    main()
