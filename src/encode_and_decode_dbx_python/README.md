Encode And Decode
Medium
String
Interview Stages
Screening
Onsite
Frequency
Asked By

Last Reported
5 days ago
Given an array of non-negative integers, design an encoder and decoder that compresses the sequence into a human-readable list of run descriptors and can restore it back to the original array, using two types of runs: Run-Length Encoding (RLE) and Bit-Packing (BP).

The encoder outputs a list of strings, each representing a run in one of the following formats:

RLE Run: Consecutive identical values are represented as "RLE[value, count]", where:

value is the repeated integer.
count is the number of consecutive occurrences.
RLE is used for runs of 8 or more repeats (except the last RLE run, which may be shorter).
Example: [1, 1, 1, 1, 1, 1, 1, 1] → "RLE[1,8]"

BP Run: Groups of up to 8 (non-identical) values are packed as "BP[v1, v2, ..., vk]", where:

Exactly 8 values per run (except the last BP run, which may have fewer).
v1, v2, ..., vk are the sequence values in order.
Example: [1, 2, 3, 4, 5, 6, 7, 8] → "BP[1,2,3,4,5,6,7,8]"

Additional Rules:

RLE runs continue as long as the value remains the same.
Default to RLE when eligible and use BP only if the next run of identical values doesn't meet the minimum length requirement of RLE.
The encoder may interleave RLE and BP runs as needed (e.g., [RLE, BP, RLE, RLE, BP, ...]) based on the encoding rules.
Implement the following methods:

String[] encode(int[] values) Encodes the input array into an array of run descriptor strings.

int[] decode(String[] runs) Decodes the array of run descriptors back to the original array.

Constraints:

1 ≤ values.length ≤ 
10
5
10 
5
 
0 ≤ values[i] < 
10
5
10 
5
 
The total length of the output after decoding must equal the input length.
Example 1:

Input: values = [5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 3]
Output: [5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 3]
Explanation: The input should be encoded as ["RLE[5,8]", "BP[1,2,3]"], since the first eight 5s form an RLE run, and the remaining values [1, 2, 3] make up a BP block. The steps are as follows:

encode([5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 3]); // Returns ["RLE[5,8]","BP[1,2,3]"].
decode(["RLE[5,8]", "BP[1,2,3]"]); // Returns [5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 3], by expanding the RLE run and unpacking the BP block.
After decoding, the output is the same as the input.

Example 2:

Input: values = [1, 1, 1]
Output: [1, 1, 1]
Explanation: All values are encoded as an RLE run since the sequence consists entirely of repeating numbers. Since this is the only RLE run, it is not required to meet the minimum length requirement.

encode([1, 1, 1]); // Returns ["RLE[1,3]"].
decode(["RLE[1,3]"]); // Returns [1, 1, 1].
Example 3:

Input: values = [1, 1, 1, 1, 2, 3, 4, 5]
Output: [1, 1, 1, 1, 2, 3, 4, 5]
Explanation: All values are encoded as a BP run since they do not meet the minimum length required for RLE. Since this is the only BP run, it is not required to meet the length requirement.

encode([1, 1, 1, 1, 2, 3, 4, 5]); // Returns ["BP[1,1,1,1,2,3,4,5]"].
decode(["BP[1,1,1,1,2,3,4,5]"]); // Returns [1, 1, 1, 1, 2, 3, 4, 5].
