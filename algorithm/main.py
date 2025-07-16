from typing import List


class Leetcode:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        209. Minimum Size Subarray Sum
        슬라이딩 윈도우 
        """
        left = 0
        right = 0
        total = 0
        min_len = float("inf")

        # left는 고정한 채 right를 하나씩 증가시킨다
        for right in range(len(nums)):
            total += nums[right]

            # left는 조건을 만족할 때만 하나씩 증가시킨다. 한번 증가한 left는 그대로 유지된다. 
            while total >= target:
                min_len = min(min_len, right - left + 1)
                total -= nums[left]
                left += 1

        # 시간복잡도:
        # right는 n번 반복 
        # left는 while문 안에서 최대 n번 증가
        # 총 이동 횟수는 O(2n) = O(n)
        # 만약 left가 매번 0부터 다시 시작하는 구조였다면 O(n^2)이었을 것
        return min_len if min_len != float("inf") else 0
