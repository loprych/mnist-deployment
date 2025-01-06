import json
import numpy as np

def create_digit_pattern(digit):
    """Create test patterns for different digits"""
    image = np.zeros(784)
    
    patterns = {
        0: [(i, j) for i in range(5, 23) for j in range(5, 23) 
            if ((i == 5 or i == 22) and 5 <= j <= 22) or 
               ((j == 5 or j == 22) and 5 <= i <= 22)],
        
        1: [(i, 14) for i in range(5, 23)] + 
           [(21, j) for j in range(12, 15)] +
           [(6, j) for j in range(13, 15)],
        
        2: [(5, j) for j in range(5, 23)] +
           [(22, j) for j in range(5, 23)] +
           [(i, 22) for i in range(5, 14)] +
           [(i, 5) for i in range(14, 23)] +
           [(13, j) for j in range(5, 23)],
        
        3: [(5, j) for j in range(5, 23)] +
           [(22, j) for j in range(5, 23)] +
           [(13, j) for j in range(5, 23)] +
           [(i, 22) for i in range(5, 23)],
        
        4: [(i, 6) for i in range(5, 14)] +
           [(13, j) for j in range(5, 23)] +
           [(i, 22) for i in range(5, 23)],
    }
    
    if digit in patterns:
        for i, j in patterns[digit]:
            image[i * 28 + j] = 1.0
            
    return image.tolist()

def get_curl_command(digit):
    """Generate curl command for testing a specific digit"""
    image = create_digit_pattern(digit)
    return f'''curl -X POST \\
  -H "Content-Type: application/json" \\
  -d \'{{"image": {json.dumps(image)}}}\' \\
  http://localhost:5000/predict'''

# Print test commands for digits 0-4
for digit in range(5):
    print(f"\n=== Test command for digit {digit} ===")
    print(get_curl_command(digit))