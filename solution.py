# design a data structure find the highest frequent item:
# Coding: OOD + data structure: 设计一个API，有两个函数，第一个每call一次收集一个购买物品的ID以及时间，第二个query最经常被购买的k个物品的list
# follow-up：第二个函数变成单位时间内被购买的最多的产品，数据结构和query该怎么改动
# follow-up：如果有很多个线程同时在call这俩function，数据结构和query该怎么改动


import heapq


class Find_Highest_Frequent:
	def __init__(self):
		self.__call_history = {}	# item_id : [timestamp]
	
	def call_collector(self, item_id, timestamp):
		if item_id not in self.__call_history:
			self.__call_history[item_id] = [timestamp]
		else:
			self.__call_history[item_id].append(timestamp)
	
	# original solution
	# def find_top(self, k):
	# 	if k < len(self.__call_history):
	# 		k = len(self.__call_history)
		
	# 	min_heap = []
	# 	for item_id in self.__call_history:
	# 		time_stamps = self.__call_history[item_id]
	# 		heapq.heappush(min_heap, (len(time_stamps), item_id))
	# 		if len(min_heap) > k:
	# 			heapq.heappop(min_heap)
		
	# 	# time complexity O(nlogk)
				
	# 	return sorted([a[1] for a in min_heap], reverse = True)

	# follow up solution
	def find_top(self, k, start, end):
		if k < len(self.__call_history):
			k = len(self.__call_history)
		
		min_heap = []
		for item_id in self.__call_history:
			time_stamps = self.__call_history[item_id]
			
			valid_time_count = self.__time_count(time_stamps, start, end)

			heapq.heappush(min_heap, (valid_time_count, item_id))
			if len(min_heap) > k:
				heapq.heappop(min_heap)
		
		# binary search time complexity O(nlogm), where m is the average # of timestamps for each item
		# heap time complexity O(nlogk), where n is # of items, k is the parameter
		# overall time complexity is O(nlogm + nlogn)		
		
		return sorted([a[1] for a in min_heap], reverse = True)

	def __time_count(self, time_stamps, start, end):
		if not start and not end:
			return len(time_stamps)
		
		# do 2 binary searches to locate start and end respectively
		if start:
			start_index = self.__binary_search(time_stamps, start, "right")
		if end:
			end_index = self.__binary_search(time_stamps, end, "left")

		if not start_index or not end_index:
			return 0
		return end_index - start_index + 1

	def __binary_search(self, time_stamps, target, edge):
		left, right = 0, len(time_stamps) - 1
		while left + 1 < right:
			mid = (left + right) // 2
			if time_stamps[mid] < target:
				left = mid
			else:
				right = mid
		
		if edge == 'right':
			if time_stamps[right] < target:
				return None
			if time_stamps[left] >= target:
				return left
			return right

		if edge == 'left':
			if time_stamps[left] > target:
				return None
			if time_stamps[right] <= target:
				return right
			return left
