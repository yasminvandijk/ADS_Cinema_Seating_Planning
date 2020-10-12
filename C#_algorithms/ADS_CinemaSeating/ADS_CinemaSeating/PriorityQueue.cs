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

        public bool Empty()
        {
            return _queue.Count == 0;
        }

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

        public T Get()
        {
            PrioritizedItem prioritizedItem = _queue[0];

            Swap(0, _queue.Count - 1);
            _queue.RemoveAt(_queue.Count - 1);
            MinHeapify(0);

            return prioritizedItem.Item;
        }

        public void TrimQueueSize(int maxSize)
        {
            while (_queue.Count > maxSize)
            {
                _queue.RemoveAt(_queue.Count - 1);
            }
        }
    }
}
