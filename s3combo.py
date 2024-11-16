import argparse
import requests
import os


def print_ascii_art():
    """Print ASCII art for S3COMBO."""
    ascii_art = r"""
  ______    ______     ______    ___   ____    ____  ______      ___    
.' ____ \  / ____ `. .' ___  | .'   `.|_   \  /   _||_   _ \   .'   `.  
| (___ \_| `'  __) |/ .'   \_|/  .-.  \ |   \/   |    | |_) | /  .-.  \ 
 _.____`.  _  |__ '.| |       | |   | | | |\  /| |    |  __'. | |   | | 
| \____) || \____) |\ `.___.'\\  `-'  /_| |_\/_| |_  _| |__) |\  `-'  / 
 \______.' \______.' `.____ .' `.___.'|_____||_____||_______/  `.___.'  

    S3 Bucket Enumeration & Combination Tool
    """
    print(ascii_art)


def fetch_permutations_from_urls(file_path):
    """Read URLs from a local file and fetch permutations."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Permutation file not found: {file_path}")

    permutations = set()
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        try:
            print(f"Fetching permutations from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            permutations.update(line.strip() for line in response.text.splitlines() if line.strip())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from {url}: {e}")

    return sorted(permutations)


def read_base_names(input_source, is_file):
    """Read base names from a string or file."""
    if is_file:
        if not os.path.isfile(input_source):
            raise FileNotFoundError(f"File not found: {input_source}")
        with open(input_source, 'r') as f:
            return [line.strip() for line in f.readlines()]
    else:
        return [name.strip() for name in input_source.split(',')]


def generate_bucket_names(base_names, permutations):
    """Generate S3 bucket names with permutations."""
    generated_names = set()
    for base in base_names:
        for perm in permutations:
            generated_names.add(f"{perm}{base}")
            generated_names.add(f"{base}{perm}")
    return sorted(generated_names)


def save_to_file(output_file, bucket_names):
    """Save the generated bucket names to a file."""
    with open(output_file, 'w') as f:
        f.write('\n'.join(bucket_names))
    print(f"Generated S3 bucket names saved to: {os.path.abspath(output_file)}")
    return os.path.abspath(output_file)


def main():
    print_ascii_art()  # Print ASCII art at the start

    parser = argparse.ArgumentParser(description="S3 Bucket Enumeration Name Generator")
    parser.add_argument('-n', '--name', help="Base name(s) for buckets (comma-separated)", required=False)
    parser.add_argument('-nL', '--name-list', help="File containing base names", required=False)
    parser.add_argument('-o', '--output', help="Output file name and location", required=True)

    args = parser.parse_args()

    # Validate arguments
    if not args.name and not args.name_list:
        parser.error("Either --name or --name-list must be provided.")
    if args.name and args.name_list:
        parser.error("Provide either --name or --name-list, not both.")

    # Get base names
    is_file = bool(args.name_list)
    input_source = args.name_list if is_file else args.name
    base_names = read_base_names(input_source, is_file)

    # Fetch permutations from URLs listed in permutations.txt
    permutations_file = "permutations.txt"
    try:
        permutations = fetch_permutations_from_urls(permutations_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"Please create a file named '{permutations_file}' in the same directory and add URLs like these:")
        print("https://raw.githubusercontent.com/cujanovic/goaltdns/master/words.txt")
        print("https://raw.githubusercontent.com/jordanpotti/AWSBucketDump/master/BucketNames.txt")
        return

    # Generate S3 bucket names
    bucket_names = generate_bucket_names(base_names, permutations)

    # Save output and print summary
    output_file_path = save_to_file(args.output, bucket_names)
    print(f"Total permutations created: {len(bucket_names)}")
    print(f"Output file location: {output_file_path}")


if __name__ == "__main__":
    main()
