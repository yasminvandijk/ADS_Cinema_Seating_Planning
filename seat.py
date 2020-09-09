import copy

neighbours_index = [[-1, -1], [-1, 0], [-1, 1], [0, -2], [0, -1], [0, 1], [0, 2], [1, -1], [1, 0], [1, 1]]

class Cinema(object):
    def __init__(self, n, m, l):
        self.n = n
        self.m = m
        self.seats = copy.copy(l)
        self.occupied_seats = copy.copy(l)
    
    def __str__(self):
        print(self.seats)
    
    def arrange(self, group):
        for i in range(self.n):
            indices = self.count_seats(group, i)
            # print(indices)
            if indices != (-1, -1): # we found a seat
                self.occupy_seats(group, indices[0], indices[1])
                self.mark_unavailable(group, indices[0], indices[1])
                print(self.seats)
   
    def count_seats(self, group, i):
        count = 0
        index = None
        for j in range(self.m): # 00, 01, 02, ...
            if self.occupied_seats[i][j] == '1' and self.can_seat(i, j):
                if count == 0:
                    index = j
                count += 1

            if count >= group:
                return (i, index)

            if self.occupied_seats[i][j] == '0':
                count = 0
        # if count == self.m - 1:
        return (-1, -1)

    def can_seat(self, i, j): # check if seat and indices i, j is available
        if self.occupied_seats[i][j] == '1':
            for indices in neighbours_index: # check if seat within matrix bounds
                if (self.n > i + indices[0] > 0 and self.m > j + indices[1] > 0):
                    # print('neighbours clear')
                    if self.occupied_seats[i + indices[0]][j + indices[1]] == 'x': # if nearby seats are occupied
                        # print('')
                        return False
            return True
        
        return False

    def mark_unavailable(self, group, i, j):
        for member in range(group):
            for indices in neighbours_index: # check if seat within matrix bounds
                if (self.n > i + indices[0] >= 0 and self.m > j + member + indices[1] >= 0):
                    # print('neighbours clear')
                    if self.occupied_seats[i + indices[0]][j + member + indices[1]] != 'x': # if nearby seats are occupied
                        self.occupied_seats[i + indices[0]][j + member + indices[1]] = '+'
                        # print(self.seats)
    
    def occupy_seats(self, group, i, j):
        for member in range(group):
            self.occupied_seats[i][j + member] = 'x'
            self.seats[i][j + member] = 'x'


if __name__ == '__main__':
    n = int(input())    # number of lines
    m = int(input())    # number of columns
    l = []
    for _ in range(n):
        l.append([b for b in input()])
    groups = list(map(int, input().split()))
    
    cinema = Cinema(n, m, l)
    cinema.arrange(2)
    cinema.arrange(1)
    # print(cinema.occupied_seats)



 # def arrange(self, group, n_group, i, j):  # here comes the strategy implementation
    #     print(f'i = {i}, j = {j}, n_group = {n_group}')
    #     # print('here')
    #     if n_group == 0:    # if we sat everyone
    #         print('sat all')
    #         # return True
    #     # if not self.can_seat(i, j) and n_group > 0: # if there are no more spaces available to finish seating everyone
    #     #     return False
    #     if i == self.n and j == self.m and n_group > 0:
    #         print('could not seat')
    #         return
    #         # return False
    #     # print('here2')
        
    #     if self.can_seat(i, j):
    #         self.occupied_seats[i][j] = 'x'
    #         n_group -= 1
    #         print('can seat')
    #         if j + 1 >= self.n: # if we reached the end of the line, wrap around
    #             print('endline')
    #             if n_group > 0:
    #                 n_group = group
    #         self.arrange(group, n_group, i + 1, 0)
    #         self.occupied_seats[i][j] = '1'
    #         print('deoccupy')
    #     else:
    #         # print('not endline')
    #         self.arrange(group, n_group, i, j + 1)
        
        # if self.occupied_seats[i][j] == 'x':
            
            # n_group += 1
        # print('here3')