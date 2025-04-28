import struct
import numpy as np
import os

def load_embedding_with_header(file_path: str):

    """
    Load embedding file saved with structure:
    [person_id][name_length][name_bytes][num_embeddings][embedding_size][embedding_data]
    """

    with open(file_path, 'rb') as f:
        # Person ID
        person_id_bytes = f.read(4)
        person_id = struct.unpack('i', person_id_bytes)[0]

        # Name Length
        name_length_bytes = f.read(4)
        name_length = struct.unpack('i', name_length_bytes)[0]

        # Name
        name_bytes = f.read(name_length)
        person_name = name_bytes.decode('utf-8')

        # Number of Embeddings
        num_embeddings_bytes = f.read(4)
        num_embeddings = struct.unpack('i', num_embeddings_bytes)[0]

        # Embedding Size
        embedding_size_bytes = f.read(4)
        embedding_size = struct.unpack('i', embedding_size_bytes)[0]

        # Embedding Data
        embedding_data_bytes = f.read(num_embeddings * embedding_size * 4)  # mỗi float32 = 4 bytes
        embeddings = np.frombuffer(embedding_data_bytes, dtype=np.float32)
        embeddings = embeddings.reshape((num_embeddings, embedding_size))

    return {
        "person_id": person_id,
        "person_name": person_name,
        "num_embeddings": num_embeddings,
        "embedding_size": embedding_size,
        "embeddings": embeddings,
    }

if __name__ == "__main__":
    result = load_embedding_with_header("7.bin")

    print("Person ID:", result["person_id"])
    print("Person Name:", result["person_name"])
    print("Num Embeddings:", result["num_embeddings"])
    print("Embedding Size:", result["embedding_size"])
    print("Embeddings Shape:", result["embeddings"].shape)
    # Get and print file size
    file_size_bytes = os.path.getsize("7.bin")
    print(f"File size: {file_size_bytes} bytes")

    # Convert to human-readable format
    if file_size_bytes < 1024:
        file_size_str = f"{file_size_bytes} bytes"
    elif file_size_bytes < 1024 * 1024:
        file_size_str = f"{file_size_bytes / 1024:.2f} KB"
    else:
        file_size_str = f"{file_size_bytes / (1024 * 1024):.2f} MB"

    print(f"File size (human-readable): {file_size_str}")

    # Nếu muốn in giá trị cụ thể:
    print(result["embeddings"])