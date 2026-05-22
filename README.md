# test_script

## Project Overview

This project demonstrates a local AI workflow built around a LoRA adapter, a merge script, `llama.cpp`, Ollama, and GGUF conversion.

The typical flow is:

1. Start from a base Hugging Face model.
2. Apply the LoRA adapter stored in `laptop-ai-lora/`.
3. Run `merge.py` to merge the adapter into the base model weights.
4. Use `llama.cpp` to convert the merged model into GGUF format.
5. Create and run a local Ollama model from the generated GGUF file.

This repository is intentionally kept lightweight for GitHub. Large generated assets such as merged model outputs, GGUF files, virtual environments, and build folders should stay out of version control.

## Project Structure

```text
test_script/
├── laptop-ai-lora/
├── llama.cpp/
├── merge.py
├── Modelfile
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.10+
- Ollama
- Git
- `llama.cpp`

## Clone Project

```bash
git clone <repo-url>
cd test_script
```

## Create Virtual Environment

### Ubuntu / Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Merge LoRA

This step loads the base model, applies the LoRA adapter from `laptop-ai-lora/`, and saves the merged result into `merged-model/`.

```bash
python merge.py
```

## Build llama.cpp

If you do not already have `llama.cpp`, clone and build it:

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

### Ubuntu Notes

If `cmake` is missing, install it with your package manager before building.

### Windows Notes

Run the build commands in PowerShell or a Developer Command Prompt with CMake installed.

## Convert to GGUF

After merging, convert the Hugging Face model into GGUF format from inside the `llama.cpp` directory:

```bash
python convert_hf_to_gguf.py ../merged-model --outfile model.gguf --outtype q8_0
```

This creates `model.gguf`, which should remain untracked in Git.

## Create Ollama Model

Go back to the project root and create a `Modelfile` with:

```text
FROM ./llama.cpp/model.gguf
```

Then build the Ollama model:

```bash
ollama create myai -f Modelfile
```

## Run Model

```bash
ollama run myai
```

## Notes

- `merge.py` currently uses `mistralai/Mistral-7B-Instruct-v0.3` as the base model.
- Make sure Ollama is installed and running before calling `ollama create` or `ollama run`.
- Keep `merged-model/`, `*.gguf`, `venv/`, and `llama.cpp/build/` out of Git to keep the repository small and push-friendly.
