# 6. Python Data Encoding for Network Transmission

All data (strings, numbers, containers) must be converted to byte sequences (binary data) before transmission.

## 6.1 String Encoding/Decoding

| Operation | Direction | Description |
|-----------|-----------|-------------|
| **encode** | Data → Binary | Converts human-readable data to transmittable binary format |
| **decode** | Binary → Data | Converts binary data back to human-readable format |

### 6.1.1 Example

```python
# String to binary (encode)
original_string = "hello world"
byte_data = original_string.encode()
print(f"Original: {original_string}")
print(f"Encoded:  {byte_data}")
# Output: b'hello world'

# Binary back to string (decode)
decoded_string = byte_data.decode()
print(f"Decoded:  {decoded_string}")
# Output: hello world

# Non-ASCII characters (e.g., Chinese)
chinese_text = "你好世界"
byte_data_cn = chinese_text.encode('utf-8')
print(f"Original: {chinese_text}")
print(f"Encoded:  {byte_data_cn}")
# Output: b'\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c'

decoded_cn = byte_data_cn.decode('utf-8')
print(f"Decoded:  {decoded_cn}")
# Output: 你好世界
```

**Key points:**
- `encode()` converts string to bytes (default encoding is UTF-8)
- `decode()` converts bytes back to string
- The `b` prefix indicates byte sequences
- Non-ASCII characters (Chinese, emoji, etc.) require UTF-8 encoding

## 6.2 Container Data (Lists, Dictionaries)

Containers cannot be directly encoded. Must be converted to string first (e.g., JSON), then encoded to binary.

### 6.2.1 Process

Container → String (JSON) → Binary Data

### 6.2.2 Example

```python
list1 = ['apple', 'banana', 'watermelon']
# Step 1: Convert list to JSON string
str_list = json.dumps(list1)  # '["apple", "banana", "watermelon"]'
# Step 2: Encode string to binary
bytelist = str_list.encode()   # b'[...]'

# Reverse process:
strinfo2 = bytelist.decode()   # JSON string
list2 = json.loads(strinfo2)   # Original list
```
