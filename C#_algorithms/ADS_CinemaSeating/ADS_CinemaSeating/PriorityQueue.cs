using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ADS_CinemaSeating
{
    public class MaxPriorityQueue<T>
    {
        private class PrioritizedItem
        {
            public int Priority { get; set; }
            public T Item { get; set; }
        }

        private List<PrioritizedItem> _queue = new List<PrioritizedItem>();

        public MaxPriorityQueue() { }

        /// <summary>
        /// swap two items in the queue
        /// </summary>
        /// <param name="index1"></param>
        /// <param name="index2"></param>
        private void Swap(int index1, int index2)
        {
            PrioritizedItem temp = _queue[index1];
            _queue[index1] = _queue[index2];
            _queue[index2] = temp;
        }

        /// <summary>
        /// get the queue index for the parent of an item at the given index
        /// </summary>
        /// <param name="index"></param>
        /// <returns></returns>
        private int ParentIndex(int index)
        {
            return (int)Math.Floor((index - 1) / 2.0);
        }

        /// <summary>
        /// get the queue index for the left child of an item at the given index
        /// </summary>
        /// <param name="index"></param>
        /// <returns></returns>
        private int LeftChildIndex(int index)
        {
            return 2 * index + 1;
        }

        /// <summary>
        /// get the queue index for the right child of an item at the given index
        /// </summary>
        /// <param name="index"></param>
        /// <returns></returns>
        private int RightChildIndex(int index)
        {
            return 2 * index + 2;
        }

        /// <summary>
        /// restores the order in the priority queue with the item at index as root node
        /// </summary>
        /// <param name="index"></param>
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
        /// check if queue is empty
        /// </summary>
        /// <returns></returns>
        public bool Empty()
        {
            return _queue.Count == 0;
        }

        /// <summary>
        /// add an item with a priority to the queue
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

            // swap item with its parent its priority is higher than the parents priority
            int index = _queue.Count - 1;
            while (index > 0 && _queue[ParentIndex(index)].Priority < _queue[index].Priority)
            {
                Swap(index, ParentIndex(index));
                index = ParentIndex(index);
            }
        }

        /// <summary>
        /// get the first item from the queue
        /// (item with the highest priority)
        /// </summary>
        /// <returns></returns>
        public T Get()
        {
            PrioritizedItem prioritizedItem = _queue[0];

            Swap(0, _queue.Count - 1);
            _queue.RemoveAt(_queue.Count - 1);
            MinHeapify(0);

            return prioritizedItem.Item;
        }

        /// <summary>
        /// trim queue size to the given maxsize,
        /// item at the back of the queue are trimmed first
        /// </summary>
        /// <param name="maxSize"></param>
        public void TrimQueueSize(int maxSize)
        {
            while (_queue.Count > maxSize)
            {
                _queue.RemoveAt(_queue.Count - 1);
            }
        }
    }
}
