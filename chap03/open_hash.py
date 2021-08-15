from __future__ import annotations
from typing import Any, Type
from enum import Enum
import hashlib

class Status(Enum):
    Occupied=0
    Empty=1
    Deleted=2

class Bucket:
    def __init__(self, key: Any=None, value:Any=None,
                 stat: Status =Status.Empty) -> None:
        self.key=key
        self.value=value
        self.stat=stat

    def set(self, key: Any, value:any, stat:Status) -> None:
        self.key=key
        self.value=value
        self.stat=stat

    def set_status(self, stat:Status) -> None:
        self.stat=stat

class OpenHash:
    def __init__(self, capacity: int) -> None:
        self.capacity=capacity
        self.table=[Bucket()] * self.capacity

    def hash_value(self, key:any)->int:
        if isinstance(key, int):
            return key%self.capacity
        return (int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.capacity)

    def rehash_value(self, key:any)->int:
        return(self.hash_value(key)+1) % self.capacity
    
    def search_node(self, key:any)->any:
        hash=self.hash_value(key)
        p=self.table[hash]

        for i in range(self.capacity):
            if p.stat==Status.Empty:
                break
            elif p.stat==Status.Occupied and p.key==key:
                return p
            hash=self.rehash_value(hash)
            p=self.table[hash]
        return None

    def search(self, key:any)->any:
        p=self.search_node(key)
        if p is not None:
            return p.value
        else:
            return None

    def add(self, key:any, value: any)->bool:
        if self.search(key) is not None:
            return False # 이미 등록된 키임.

        hash=self.hash_value(key)
        p=self.table[hash]
        for i in range(self.capacity):
            if p.stat==Status.Empty or p.stat==Status.Deleted:
                self.table[hash]=Bucket(key, value, Status.Occupied)
                return True
            hash=self.rehash_value(hash)
            p=self.table[hash]
        return False
    
    def remove(self, key:any)->int:
        p=self.search_node(key)
        if p is None:
            return False
        p.set_status(Status.Deleted)
        return True

    def dump(self)->None:
        for i in range(self.capacity):
            print(f'{i:2} ', end='')
            if self.table[i].stat==Status.Occupied:
                print(f'{self.table[i].key} ({self.table[i].value})')
            elif self.table[i].stat==Status.Empty:
                print('--미등록--')
            elif self.table[i].stat==Status.Deleted:
                print('--삭제 완료')
                
