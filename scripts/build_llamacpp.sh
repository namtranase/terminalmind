cd llama.cpp
mkdir -p build
rm -rf build/*
cd build
cmake .. -DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS
cmake --build . --config Release -- -j$(nproc)

cd ../..
cp llama.cpp/build/bin/main temi-packaging/usr/local/bin/temicore
