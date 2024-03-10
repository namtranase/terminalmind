if [! -d llama.cpp/build ]; then
    echo "Building the llamacpp ..."
    cd llama.cpp
    mkdir -p build
    rm -rf build/*
    cd build
    cmake .. -DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS
    cmake --build . --config Release -- -j$(nproc)
    cd ../..
fi

echo "Starting the llamcpp server ..."
./llama.cpp/build/bin/server -m /home/namtd/workspace/personal/kicopilot/playground/models/model.gguf -c 128 --host 0.0.0.0 --port 8080
