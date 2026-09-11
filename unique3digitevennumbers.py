class Solution:
    def totalNumbers(self, digits: List[int]) -> int:
        available_counts = Counter(digits)
        unique_even_count = 0

        for num in range(100, 1000, 2):
            # Extract individual digits
            hundreds = num // 100
            tens = (num // 10) % 10
            ones = num % 10
            
            # Count the required digits for the current number
            required_counts = Counter([hundreds, tens, ones])
            
            # Check if we have enough of each digit to form 'num'
            valid = True
            for digit, req_count in required_counts.items():
                if available_counts[digit] < req_count:
                    valid = False
                    break
            
            if valid:
                unique_even_count += 1
                
        return unique_even_count
