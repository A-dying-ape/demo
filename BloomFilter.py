# coding=utf-8
"""实现最基本的布隆过滤器"""
import mmh3


class CountingBloomFilter:
    def __init__(self, size, hash_num):
        self.size = size
        self.hash_num = hash_num
        self.byte_array = bytearray(size)

    def add(self, s):
        for seed in range(self.hash_num):
            result = mmh3.hash(s, seed) % self.size
            if self.byte_array[result] < 256:
                self.byte_array[result] += 1

    def lookup(self, s):
        for seed in range(self.hash_num):
            result = mmh3.hash(s, seed) % self.size
            if self.byte_array[result] == 0:
                return "Nope"
        return "Probably"

    def remove(self, s):
        for seed in range(self.hash_num):
            result = mmh3.hash(s, seed) % self.size
            if self.byte_array[result] > 0:
                self.byte_array[result] -= 1


cbf = CountingBloomFilter(500000, 7)
cbf.add("a")
cbf.add("b")
cbf.remove("a")
print(cbf.lookup("a"))
print(cbf.lookup("b"))