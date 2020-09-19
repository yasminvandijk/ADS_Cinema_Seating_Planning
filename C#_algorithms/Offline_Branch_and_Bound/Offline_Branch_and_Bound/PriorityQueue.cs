using System;
using System.Collections.Generic;
using System.Text;

namespace Offline_Branch_and_Bound
{
    /// <summary>
    /// priority queue; sorts items on priority in descending order
    /// </summary>
    /// <typeparam name="T">type of the items</typeparam>
    public class MaxPriorityQueue<T>
    {
        private class PrioritizedItem
        {
            public int Priority { get; set; }
            public T Item { get; set; }
        }

        private List<PrioritizedItem> _queue = new List<PrioritizedItem>();

        /// <summary>
        /// creates an empty priority queue which sorts item on priority in descending order
        /// </summary>
        public MaxPriorityQueue() {}

        private void Swap(int index1, int index2)
        {
            PrioritizedItem temp = _queue[index1];
            _queue[index1] = _queue[index2];
            _queue[index2] = temp;
        }

        private int ParentIndex(int index)
        {
            return (int)Math.Floor((index - 1) / 2.0);
        }

        private int LeftChildIndex(int index)
        {
            return 2 * index + 1;
        }

        private int RightChildIndex(int index)
        {
            return 2 * index + 2;
        }

        private void MinHeapify(int index)
        {
            int leftChildIndex = LeftChildIndex(index);
            int rightChildIndex = RightChildIndex(index);
            
            int biggestIndex = index;

            // check if the item at this index has children with a bigger priority
            if (leftChildIndex < _queue.Count && _queue[leftChildIndex].Priority > _queue[biggestIndex].Priority)
            {
                biggestIndex = leftChildIndex;
            }
            if (rightChildIndex < _queue.Count && _queue[rightChildIndex].Priority > _queue[biggestIndex].Priority)
            {
                biggestIndex = rightChildIndex;
            }

            // if a child with a bigger priority is found swap it with its parent
            // and minheapify the subtree with biggestIndex as its root
            if (biggestIndex != index)
            {
                Swap(index, biggestIndex);
                MinHeapify(biggestIndex);
            }
        }

        /// <summary>
        /// returns whether the priority queue is empty
        /// </summary>
        /// <returns></returns>
        public bool Empty()
        {
            return _queue.Count == 0;
        }

        /// <summary>
        /// adds an item to the priority queue
        /// </summary>
        /// <param name="priority"></param>
        /// <param name="item"></param>
        public void Add(int priority, T item)
        {
            PrioritizedItem prioritizedItem = new PrioritizedItem
            {
                Priority = priority,
                Item = item
            };

            _queue.Add(prioritizedItem);

            // swap item with its parent if its priority is higher than the parents priority
            int index = _queue.Count - 1;
            while (index > 0 && _queue[ParentIndex(index)].Priority < _queue[index].Priority)
            {
                Swap(index, ParentIndex(index));
                index = ParentIndex(index);
            }
        }

        /// <summary>
        /// gets the item with the highest priority from the priority queue
        /// </summary>
        /// <returns></returns>
        public T Get()
        {
            if (_queue.Count == 0)
            {
                throw new Exception("unable to get item out of empty queue");
            }
            
            PrioritizedItem prioritizedItem = _queue[0];

            _queue[0] = _queue[_queue.Count - 1];
            MinHeapify(0);

            return prioritizedItem.Item;
        }
    }
}
