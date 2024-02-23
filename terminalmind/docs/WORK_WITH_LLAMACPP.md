# Work with llama.cpp in terminalmind
This guide provides instructions for building the main executable from the llama.cpp project and integrating it with terminalmind. Additionally, it covers the installation of GGUF models and how to switch models using the `temi` command.

## Build the main executable

```bash
cd llama.cpp
mkdir -p build
rm -rf build/*
cd build
cmake .. -DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS
cmake --build . --config Release -- -j$(nproc)
```

## Install GGUF models
You can download and use GGUF models directly from the Hugging Face repository:
```bash
git clone https://huggingface.co/namtran/Mistral-7b-v0.2-AWQ-GGUF
```

Alternatively, you can convert original LLaMA models to the GGUF format. For detailed instructions on model conversion, refer to the [llama.cpp README](https://github.com/ggerganov/llama.cpp).

## Switching models with `temi`
To change the model used by Terminalmind, use the `temi change_model` command:

```bash
temi change_model
#Please enter the new absolute path to your .gguf model file:
#/home/namtd/llm_models/model.gguf
#Model path changed successfully.
```
