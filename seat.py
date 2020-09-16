import copy
import numpy as np
neighbours_index = [[-1, -1], [-1, 0], [-1, 1], [0, -2], [0, -1], [0, 1], [0, 2], [1, -1], [1, 0], [1, 1]]

class Cinema(object):
    def __init__(self, n, m, l):
        self.n = n
        self.m = m
        self.output_seats = np.copy(l)
        self.occupied_seats = np.copy(l)
    
    def __str__(self):
        print(self.output_seats)
    
    def print_seats(self):
        for seat in self.occupied_seats:
            print(''.join(seat))
        print()  
    
    def arrange(self, group):
        # print(f'group = {group}')
        best_indices = None
        best_count = None
        for i in range(self.n):
            indices = self.count_seats(group, i)
            # print(indices)
            if indices != (-1, -1): # we found a seat
                unavailable_seats = self.count_unavailable(group, indices[0], indices[1])
                if best_count == None or unavailable_seats < best_count:
                    best_indices = indices
                    best_count = unavailable_seats

        if best_count != None:
            self.occupy_seats(group, best_indices[0], best_indices[1])
            self.mark_unavailable(group, best_indices[0], best_indices[1])
            self.print_seats()

            return True

        # self.print_seats()
        return False

   
    def count_seats(self, group, i):
        count = 0
        index = None
        for j in range(self.m): # 00, 01, 02, ...
            if self.occupied_seats[i,j] == '1':
                if count == 0:
                    index = j
                count += 1

            if count >= group:
                return (i, index)

            if self.occupied_seats[i,j] != '1':
                count = 0
        # if count == self.m - 1:
        return (-1, -1)

    def can_seat(self, i, j): # check if seat and indices i, j is available
        if self.occupied_seats[i,j] == '1':
            for indices in neighbours_index: # check if seat within matrix bounds
                if (self.n > i + indices[0] > 0 and self.m > j + indices[1] > 0):
                    # print('neighbours clear')
                    if self.occupied_seats[i + indices[0],j + indices[1]] == 'x': # if nearby seats are occupied
                        # print('')
                        return False
            return True
        
        return False

    def count_unavailable(self, group, i, j):
        count = 0
        for member in range(group):
            for indices in neighbours_index: # check if seat within matrix bounds
                if (self.n > i + indices[0] >= 0 and self.m > j + member + indices[1] >= 0):
                    # print('neighbours clear')
                    if self.occupied_seats[i + indices[0],j + member + indices[1]] == '1': # if nearby seats are occupied
                        count += 1
        
        return count

    def mark_unavailable(self, group, i, j):
        for member in range(group):
            for indices in neighbours_index: # check if seat within matrix bounds
                if (self.n > i + indices[0] >= 0 and self.m > j + member + indices[1] >= 0):
                    # print('neighbours clear')
                    if self.occupied_seats[i + indices[0],j + member + indices[1]] == '1': # if nearby seats are occupied
                        self.occupied_seats[i + indices[0],j + member + indices[1]] = '+'
                        # print(self.output_seats)
    
    def occupy_seats(self, group, i, j):
        for member in range(group):
            self.occupied_seats[i,j + member] = 'x'
            self.output_seats[i,j + member] = 'x'

def recalculate_indices(groups):
    # print("group in", groups)
    multiplied_groups = [groups[i] * (i + 1) for i in range(len(groups))]
    # print(multiplied_groups)
    
    groups_indices1 = np.argsort(multiplied_groups)
    print(f'group after recalculate: {groups_indices1}')

    return np.copy(groups_indices1)

if __name__ == '__main__':
    n = int(input())    # number of lines
    m = int(input())    # number of columns
    l = np.empty((n, m), dtype = str)
    groups_indices = np.array([])
    for i in range(n):
       l[i] = [b for b in input()]
    groups = np.array(list(map(int, input().split())))
    
    groups_indices = recalculate_indices(groups)
    cinema = Cinema(n, m, l) 
    
    count = 0
    arranged = False
    i = len(groups_indices) - 1
    while i >= 0:
    # for i in range(len(groups)):
        if groups[groups_indices[i]] > 0:
            if cinema.arrange(groups_indices[i] + 1):
                count = count + groups_indices[i] + 1
                # arranged = True
           
            groups[groups_indices[i]] -= 1
            print("group before", groups_indices)
            rec_groups_indices = recalculate_indices(groups)
            print("recalculated group:", rec_groups_indices)
            if np.array_equal (rec_groups_indices, groups_indices):
                i = len(groups_indices)
            else:
                groups_indices = copy.deepcopy(rec_groups_indices)
                print("changed group_indec:", groups_indices)
        i -= 1    
        #    arranged = False

    cinema.print_seats()
    print(f'people seated: {count}')
