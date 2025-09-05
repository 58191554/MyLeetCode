Design a data structure SnapshotSet that functions as a set of integers and supports four operations: adding an element, removing an element, checking for existence, and creating a snapshot iterator.

When an iterator is created, it must iterate over exactly the elements present in the set at that time, preserving the insertion order as they were added to the set. Changes to the set after the iterator's creation must not affect the iterator.

Implement the SnapshotSet class with the following methods:

boolean add(int n): Adds n to the set if not already present. Returns true if the element was newly added, or false if it already existed.
boolean remove(int n): Removes n from the set if present. Returns true if the element was removed, or false if it was not found.
boolean contains(int n): Returns true if n is currently in the set, otherwise returns false.
Iterator getIterator(): Returns an iterator that traverses the elements present in the set at the time this method is called, in the order they were added. Subsequent modifications to the set must not affect this iterator.
Each iterator returned by getIterator() must support the following methods:

hasNext(): Returns true if there are remaining elements to iterate, or false otherwise.
next(): Returns the next element in the snapshot in insertion order. Throw an exception if the next element doesn't exist.
Additional Requirement:

Your design must allow multiple iterators to exist independently, each reflecting the set's state at its own creation time.
All primary operations should run in amortized O(1) time.
Space complexity should not exceed O(N+M), where N is the current number of elements added to the set, M is the number of iterators created. This ensures efficient space usage even if many iterators are created.
Example:

Input:
["SnapshotSet", "add", "add", "add", "add", "add", "getIterator", "remove", "remove", "remove", "getIterator"]
[[], [1], [2], [3], [4], [1], [], [1], [3], [5], []]
Output:
[null, true, true, true, true, false, [1, 2, 3, 4], true, true, false, [2, 4]]
Explanation:

SnapshotSet set = new SnapshotSet();
set.add(1); // Returns true.
set.add(2); // Returns true.
set.add(3); // Returns true.
set.add(4); // Returns true.
set.add(1); // Returns false.
Iterator<Integer> it1 = set.getIterator(); // Returns a snapshot iterator over elements: [1, 2, 3, 4].
set.remove(1); // Returns true.
set.remove(3); // Returns true.
set.remove(5); // Returns false.
Iterator<Integer> it2 = set.getIterator(); // Returns a snapshot iterator over elements: [2, 4].
By calling it1.hasNext() and it1.next() alternately, the iterator should return [1, 2, 3, 4].
By calling it2.hasNext() and it2.next() alternately, the iterator should return [2, 4].
