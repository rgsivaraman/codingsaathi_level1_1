# Example Agents

This document contains example agent code snippets you can use in the Agent Marketplace.

## 1. Text Reverser

**Description**: Reverses any input text

**Code**:
```python
text = input_data.get('text', '')
result = text[::-1]
```

**Input Example**:
```json
{"text": "Hello World"}
```

**Output**: `dlroW olleH`

---

## 2. Word Counter

**Description**: Counts words in a text

**Code**:
```python
text = input_data.get('text', '')
word_count = len(text.split())
result = f"Word count: {word_count}"
```

**Input Example**:
```json
{"text": "This is a sample text"}
```

**Output**: `Word count: 5`

---

## 3. Text Case Converter

**Description**: Converts text to uppercase, lowercase, or title case

**Code**:
```python
text = input_data.get('text', '')
mode = input_data.get('mode', 'upper')

if mode == 'upper':
    result = text.upper()
elif mode == 'lower':
    result = text.lower()
elif mode == 'title':
    result = text.title()
else:
    result = "Invalid mode. Use 'upper', 'lower', or 'title'"
```

**Input Example**:
```json
{"text": "hello world", "mode": "title"}
```

**Output**: `Hello World`

---

## 4. Simple Calculator

**Description**: Performs basic arithmetic operations

**Code**:
```python
num1 = input_data.get('num1', 0)
num2 = input_data.get('num2', 0)
operation = input_data.get('operation', 'add')

if operation == 'add':
    result = num1 + num2
elif operation == 'subtract':
    result = num1 - num2
elif operation == 'multiply':
    result = num1 * num2
elif operation == 'divide':
    if num2 != 0:
        result = num1 / num2
    else:
        result = "Error: Division by zero"
else:
    result = "Invalid operation"
```

**Input Example**:
```json
{"num1": 10, "num2": 5, "operation": "multiply"}
```

**Output**: `50`

---

## 5. List Sorter

**Description**: Sorts a list of numbers

**Code**:
```python
numbers = input_data.get('numbers', [])
reverse = input_data.get('reverse', False)

sorted_numbers = sorted(numbers, reverse=reverse)
result = f"Sorted: {sorted_numbers}"
```

**Input Example**:
```json
{"numbers": [5, 2, 8, 1, 9], "reverse": false}
```

**Output**: `Sorted: [1, 2, 5, 8, 9]`

---

## 6. Palindrome Checker

**Description**: Checks if a text is a palindrome

**Code**:
```python
text = input_data.get('text', '')
clean_text = ''.join(c.lower() for c in text if c.isalnum())
is_palindrome = clean_text == clean_text[::-1]
result = f"'{text}' is {'a palindrome' if is_palindrome else 'not a palindrome'}"
```

**Input Example**:
```json
{"text": "A man a plan a canal Panama"}
```

**Output**: `'A man a plan a canal Panama' is a palindrome`

---

## 7. Temperature Converter

**Description**: Converts temperature between Celsius and Fahrenheit

**Code**:
```python
temp = input_data.get('temperature', 0)
from_unit = input_data.get('from', 'C')
to_unit = input_data.get('to', 'F')

if from_unit == 'C' and to_unit == 'F':
    result = (temp * 9/5) + 32
    result = f"{temp}°C = {result}°F"
elif from_unit == 'F' and to_unit == 'C':
    result = (temp - 32) * 5/9
    result = f"{temp}°F = {result}°C"
else:
    result = "Invalid conversion units"
```

**Input Example**:
```json
{"temperature": 100, "from": "C", "to": "F"}
```

**Output**: `100°C = 212.0°F`

---

## 8. Fibonacci Generator

**Description**: Generates Fibonacci sequence up to n numbers

**Code**:
```python
n = input_data.get('n', 10)
fib_sequence = []

a, b = 0, 1
for i in range(n):
    fib_sequence.append(a)
    a, b = b, a + b

result = f"Fibonacci sequence ({n} numbers): {fib_sequence}"
```

**Input Example**:
```json
{"n": 8}
```

**Output**: `Fibonacci sequence (8 numbers): [0, 1, 1, 2, 3, 5, 8, 13]`

---

## 9. Prime Number Checker

**Description**: Checks if a number is prime

**Code**:
```python
num = input_data.get('number', 2)

if num < 2:
    result = f"{num} is not prime"
else:
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    
    result = f"{num} is {'prime' if is_prime else 'not prime'}"
```

**Input Example**:
```json
{"number": 17}
```

**Output**: `17 is prime`

---

## 10. JSON Formatter

**Description**: Pretty prints JSON data

**Code**:
```python
import json

data = input_data.get('data', {})
indent = input_data.get('indent', 2)

result = json.dumps(data, indent=indent)
```

**Input Example**:
```json
{"data": {"name": "John", "age": 30, "city": "New York"}, "indent": 4}
```

**Output**:
```json
{
    "name": "John",
    "age": 30,
    "city": "New York"
}
```

---

## Tips for Creating Agents

1. **Use input_data**: Always access input through the `input_data` dictionary
2. **Set result**: Store your output in the `result` variable
3. **Handle errors**: Use try-except blocks for robust agents
4. **Provide defaults**: Use `.get()` with default values for optional inputs
5. **Document clearly**: Provide good descriptions and tags
6. **Test thoroughly**: Test with various inputs before publishing

## Restricted Functions

For security reasons, the following are NOT available in the sandbox:
- File I/O operations (open, read, write)
- Network operations (requests, urllib)
- System operations (os, sys)
- Subprocess execution
- Import statements (except json, which is pre-imported)

## Available Built-ins

The following built-in functions are available:
- `print`, `len`, `range`
- `str`, `int`, `float`, `bool`
- `list`, `dict`, `tuple`, `set`
- `abs`, `min`, `max`, `sum`
- `sorted`, `enumerate`, `zip`
- `map`, `filter`
- `json` module (pre-imported)
