# test_script

## Project Overview

This project demonstrates a complete local AI workflow using:

* LoRA adapter fine-tuning
* Hugging Face Transformers
* GGUF conversion
* `llama.cpp`
* Ollama local inference

The workflow is designed to:

1. Load a base Hugging Face model
2. Apply the trained LoRA adapter
3. Merge the LoRA weights into the base model
4. Convert the merged model into GGUF format
5. Run the final model locally using Ollama

This repository is intentionally lightweight and GitHub-friendly. Large generated assets and model weights are excluded from version control.

---

# Project Structure

```text
test_script/
├── laptop-ai-lora/
│   ├── adapter_config.json
│   ├── tokenizer.json
│   └── ...
├── llama.cpp/
├── merge.py
├── Modelfile
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Requirements

## Software

* Python 3.10+
* Git
* Ollama
* CMake
* `llama.cpp`

## Recommended Hardware

### Recommended

* NVIDIA GPU with CUDA support

### Minimum

* 16GB RAM
* Additional swap memory recommended for CPU merge workflow

---

# Download Missing Model File

This repository does NOT include:

```text
adapter_model.safetensors
```

because GitHub blocks files larger than 100MB.

Download the file separately and place it inside:

```text
laptop-ai-lora/
```

Expected structure:

```text
laptop-ai-lora/
├── adapter_model.safetensors
├── adapter_config.json
├── tokenizer.json
└── ...
```

---

# Clone Project

```bash
git clone <repo-url>
cd test_script
```

---

# Create Virtual Environment

## Ubuntu / Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Merge LoRA

This step:

* loads the base model
* applies the LoRA adapter
* merges weights
* saves output into:

```text
merged-model/
```

Run:

```bash
python merge.py
```

---

# Ubuntu Swap Memory Recommendation

For CPU-only systems or low-memory laptops:

```bash
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Check:

```bash
free -h
```

---

# Build llama.cpp

If you do not already have `llama.cpp`:

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
```

Install build tools:

## Ubuntu

```bash
sudo apt install build-essential cmake -y
```

## Windows

Install:

* Visual Studio Build Tools
* CMake

Then build:

```bash
cmake -B build
cmake --build build --config Release
```

---

# Convert to GGUF

From inside:

```text
llama.cpp/
```

run:

```bash
python convert_hf_to_gguf.py ../merged-model --outfile model.gguf --outtype q8_0
```

This generates:

```text
model.gguf
```

Do NOT commit GGUF files to GitHub.

---

# Create Ollama Model

Go back to project root:

```bash
cd ..
```

Create:

```text
Modelfile
```

Content:

```text
FROM ./llama.cpp/model.gguf
```

Then create model:

```bash
ollama create myai -f Modelfile
```

---

# Run Model

```bash
ollama run myai
```

---

# Optional Python Example

Install:

```bash
pip install ollama
```

Example:

```python
import ollama

response = ollama.chat(
    model='myai',
    messages=[
        {'role': 'user', 'content': 'Hello'}
    ]
)

print(response['message']['content'])
```

---

# Notes

* `merge.py` currently uses:

  ```text
  mistralai/Mistral-7B-Instruct-v0.3
  ```

* Ollama must be installed and running before:

  ```bash
  ollama create
  ollama run
  ```

* Large files are intentionally excluded:

  * `*.gguf`
  * `merged-model/`
  * `venv/`
  * `llama.cpp/build/`
  * `adapter_model.safetensors`

* Recommended hosting for large model files:

  * Hugging Face
  * Google Drive
  * Mega

* This project supports:

  * Ubuntu
  * Windows
  * CPU inference via Ollama
  * NVIDIA GPU workflows
