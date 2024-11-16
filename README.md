# **S3COMBO**
### S3 Bucket Enumeration & Combination Tool

S3COMBO is a Python tool for generating permutations of S3 bucket names based on base names and a set of pre-defined permutations. It simplifies the enumeration process for discovering potential S3 buckets.

---

## **Features**
- Dynamically fetch permutations from trusted online sources.
- Combine base names with permutations by prepending and appending them.
- Generate a list of bucket name permutations.
- Save results to a file for further use.
- Easily customizable and extendable.

---

## **Setup Guide**

### **Prerequisites**
1. Install Python 3.7+ on your system. [Download Python](https://www.python.org/downloads/).
2. Install the `requests` library:
   ```bash
   pip install requests
   ```
### **Installation**
```bash
 git clone https://github.com/M0M3NTUM44/s3combo.git
cd s3combo
```
   
## **Usage Guide**
1. **Generate Bucket Name Permutations with Base Names**:
   - Using a single or multiple base names (comma-separated):
     ```bash
     python s3COMBO.py -n "example,example2" -o output.txt
     ```
   - Using a file containing base names:
     ```bash
     python s3COMBO.py -nL basenames.txt -o output.txt
     ```

2. **Key Options**:
   - `-n` or `--name`: Specify base names directly (comma-separated).
   - `-nL` or `--name-list`: Provide a file containing base names (one per line).
   - `-o` or `--output`: Specify the output file name and location.

---

### **Example**
To generate permutations for the base name `mybucket` and save them to `results.txt`:
```bash
python s3COMBO.py -n "mybucket" -o results.txt
```
---
### **Edit permutation sources**
You can change the sources of the permutataion wordlists to what ever you want (as long as <curl> can reach it).
This can be done by editing the *permutations.txt* file.

