# import random
# import math
# import numpy as np
# class TabulationHash:
#     """Hash function for hashing by tabulation.
#
#     The 32-bit key is split to four 8-bit parts. Each part indexes
#     a separate table of 256 randomly generated values. Obtained values
#     are XORed together.
#     """
#
#     def __init__(self, num_buckets):
#         self.tables = [None] * 4
#         for i in range(4):
#             self.tables[i] = [random.randint(0, 0xffffffff) for _ in range(256)]
#         self.num_buckets = num_buckets
#
#     def hash(self, key):
#         h0 = key & 0xff
#         h1 = (key >> 8) & 0xff
#         h2 = (key >> 16) & 0xff
#         h3 = (key >> 24) & 0xff
#         t = self.tables
#         return (t[0][h0] ^ t[1][h1] ^ t[2][h2] ^ t[3][h3]) % self.num_buckets
#
# class CuckooTable:
#     """Hash table with Cuckoo hashing.
#
#     We have two hash functions, which map 32-bit keys to buckets of a common
#     hash table. Unused buckets contain None.
#     """
#
#     def __init__(self, num_buckets):
#         """Initialize the table with the given number of buckets.
#         The number of buckets is expected to stay constant."""
#
#         # The array of buckets
#         self.num_buckets = num_buckets
#         self.table = [None] * num_buckets
#
#         # Create two fresh hash functions
#         self.hashes = [TabulationHash(num_buckets), TabulationHash(num_buckets)]
#
#     def lookup(self, key):
#         """Check if the table contains the given key. Returns True or False."""
#
#         b0 = self.hashes[0].hash(key)
#         b1 = self.hashes[1].hash(key)
#         # print("## Lookup key={} b0={} b1={}".format(key, b0, b1))
#         return self.table[b0] == key or self.table[b1] == key
#
#     def insert_helper(self, key):
#         """Insert a new key to the table. Assumes that the key is not present yet."""
#         h0 = self.hashes[0].hash(key)
#         h1 = self.hashes[1].hash(key)
#
#         # IF INSERTION SUCCEEDS
#
#         if (self.table[h0] == key or self.table[h1] == key):
#             return None
#
#         if (self.table[h0] == None or self.table[h1] == None):
#             if (self.table[h0] == None):
#                 self.table[h0] = key
#                 return None
#             else:
#                 self.table[h1] = key
#                 return None
#
#         # IF INSERTION FAILS
#
#         # Insert the value and keep the "removed" one as key
#         self.table[h0], key = key, self.table[h0]
#
#         first_hash = h0
#         counter = 6 * math.log(self.num_buckets)
#         counter = counter - 1
#         # counter = 300
#         while (counter > 0 and key != None):
#             h = self.hashes[0].hash(key)
#             if h == first_hash:
#                  h = self.hashes[1].hash(key)
#             #swap
#             self.table[h], key = key, self.table[h]
#
#             first_hash = h
#             counter = counter - 1
#
#         return key
#
#     # def rehash(self, num_buckets):
#     #
#     #     new_arr = [None] * num_buckets * 2
#     #
#     #     oldarr = []
#     #     for i in self.table:
#     #         oldarr.append(i)
#     #
#     #     for i in oldarr:
#     #         if(i != None):
#     #             self.insert_help(i, new_arr) # new array pi qon
#     #
#     #     self.table = new_arr
#
#     def rehash(self, num_buckets):
#         temp = []
#         for i in self.table:
#             temp.append(i)
#         new_arr = [None] * num_buckets * 4
#
#         for i in temp:
#             if(i != None):
#                 self.insert_help(i,new_arr)
#
#         self.table = new_arr
#
#     def insert(self, key):
#         self.insert_help(key, self.table)
#
#     # def insert(self, key):
#     #         # print(key)
#     #         while (True):
#     #             key = self.insert_helper(key)
#     #             if(key != None):
#     #
#     #                 self.rehash(self.num_buckets)
#     #             else:
#     #
#     #                 break
#
#     def insert_helper_rec(self, key,t_id, cnt, n):
#         if(cnt == n):
#             return
#
#         h0 = self.hashes[0].hash(key)
#         h1 = self.hashes[1].hash(key)
#
#         # IF INSERTION SUCCEEDS
#
#         if (self.table[h0] == key or self.table[h1] == key):
#             return
#
#         if(self.table[t_id] != None):
#             new_t_id = None
#             temp = self.table[t_id]
#             self.table[t_id] = key
#             if(t_id == 0):
#                 new_t_id = 1
#             else:
#                 new_t_id = 0
#             self.insert_helper_rec(temp,new_t_id, cnt + 1, n)
#
#
#     def insert_help(self, key, array):
#         h0 = self.hashes[0].hash(key)
#         h1 = self.hashes[1].hash(key)
#
#         if (array[h0] == key or array[h1] == key):
#             return
#
#         if(array[h0] is None):
#             array[h0] = key
#             return
#         elif(array[h1] is None):
#             array[h1] = key
#             return
#
#         else:
#             for i in range(5):
#                 key, array[h0] = array[h0], key
#
#                 if(key == None):
#                     return
#
#                 key, array[h1] = array[h1], key
#
#                 if(key == None):
#                     return
#
#         self.rehash(self.num_buckets)
#         self.insert_help(key,array)
#


import random
import math
class TabulationHash:
    """Hash function for hashing by tabulation.

    The 32-bit key is split to four 8-bit parts. Each part indexes
    a separate table of 256 randomly generated values. Obtained values
    are XORed together.
    """

    def __init__(self, num_buckets):
        self.tables = [None] * 4
        for i in range(4):
            self.tables[i] = [random.randint(0, 0xffffffff) for _ in range(256)]
        self.num_buckets = num_buckets

    def hash(self, key):
        h0 = key & 0xff
        h1 = (key >> 8) & 0xff
        h2 = (key >> 16) & 0xff
        h3 = (key >> 24) & 0xff
        t = self.tables
        return (t[0][h0] ^ t[1][h1] ^ t[2][h2] ^ t[3][h3]) % self.num_buckets

class CuckooTable:
    """Hash table with Cuckoo hashing.

    We have two hash functions, which map 32-bit keys to buckets of a common
    hash table. Unused buckets contain None.
    """

    def __init__(self, num_buckets):
        """Initialize the table with the given number of buckets.
        The number of buckets is expected to stay constant."""

        # The array of buckets
        self.num_buckets = num_buckets
        self.table = [None] * num_buckets

        # Create two fresh hash functions
        self.hashes = [TabulationHash(num_buckets), TabulationHash(num_buckets)]

    def lookup(self, key):
        """Check if the table contains the given key. Returns True or False."""

        b0 = self.hashes[0].hash(key)
        b1 = self.hashes[1].hash(key)
        # print("## Lookup key={} b0={} b1={}".format(key, b0, b1))
        return self.table[b0] == key or self.table[b1] == key

    def insert_helper(self, key):
        """Insert a new key to the table. Assumes that the key is not present yet."""


        # IF INSERTION SUCCEEDS
        counter = 6 * math.log(self.num_buckets)
        counter -= 1
        first_hash = None

        while (counter > 0):
            h0 = self.hashes[0].hash(key)
            h1 = self.hashes[1].hash(key)
            if (self.table[h0] == key or self.table[h1] == key):
                return None

            elif (self.table[h0] == None or self.table[h1] == None):
                if (self.table[h0] == None):
                    self.table[h0] = key
                    return None
                else:
                    self.table[h1] = key
                    return None
            else:
                counter -= 1
                if first_hash == h0 or first_hash == None:
                    first_hash = h1
                    key, self.table[first_hash] = self.table[first_hash], key

                else:
                    first_hash = h0
                    key, self.table[first_hash] = self.table[first_hash], key

        return key



    def rehash(self, num_buckets):
        temp = []
        for i in self.table:
            temp.append(i)
        while(True):
            flag = True
            self.table.clear()
            self.table = [None] * num_buckets
            i = 0
            while(i < 2):
                self.hashes[i] = TabulationHash(num_buckets)
                i+=1

            for val in temp:
                if(val != None):
                    if(self.insert_helper(val) != None):
                        flag = False
                        break
            if(flag):
                break

    def insert(self, key):
        while (True):
            key = self.insert_helper(key)
            if(key != None):
                self.rehash(self.num_buckets)
            else:
                break