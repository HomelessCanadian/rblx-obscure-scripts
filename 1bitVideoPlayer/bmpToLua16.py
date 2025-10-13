from PIL import Image

# Load image
img_path = "C://Users//Homeless//Pictures//gridtest.bmp"
img = Image.open(img_path).convert("L")
width, height = img.size

print(f"📷 Image loaded: {width}x{height}")

# Get pixels as flat list
pixels = list(img.getdata())

# Threshold to binary
bitmap = [1 if p >= 128 else 0 for p in pixels]

print(f"✅ Image converted to bitmap ({len(bitmap)} pixels)")

# Chunk into 32x18 subframes
def chunk_bitmap(bitmap, width, height, sub_w=32, sub_h=18):
    chunks = []
    for sub_y in range(0, height, sub_h):
        for sub_x in range(0, width, sub_w):
            chunk = []
            for y in range(sub_y, min(sub_y + sub_h, height)):
                for x in range(sub_x, min(sub_x + sub_w, width)):
                    i = y * width + x
                    chunk.append(bitmap[i])
            
            while len(chunk) < sub_w * sub_h:
                chunk.append(0)
            
            chunks.append(chunk)
    
    return chunks

# Encode chunk to hex
def encode_chunk(chunk):
    hex_str = ""
    for i in range(0, len(chunk), 8):
        byte_bits = chunk[i:i+8]
        while len(byte_bits) < 8:
            byte_bits.append(0)
        byte_val = sum(byte_bits[j] << (7-j) for j in range(8))
        hex_str += f"{byte_val:02x}"
    return hex_str

# Build Lua output
chunks = chunk_bitmap(bitmap, width, height)
print(f"📦 Created {len(chunks)} chunks")

with open("test_frame.lua", "w") as f:
    f.write("return {\n")
    for i, chunk in enumerate(chunks):
        hex_str = encode_chunk(chunk)
        f.write(f'  section_{i+1:02d} = "{hex_str}",\n')
    f.write("}\n")

print("✅ Encoded Lua frame written to test_frame.lua")
if chunks:
    sample = encode_chunk(chunks[0])
    print(f"💡 First 32 chars of hex: {sample[:32]}")
    print(f"💡 All hex chars are 0-9,a-f? {all(c in '0123456789abcdef' for c in sample)}")
