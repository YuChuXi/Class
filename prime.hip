#include <hip/hip_runtime.h>
#include <iostream>

#define CHECK(cmd) do { \
    hipError_t error = (cmd); \
    if (error != hipSuccess) { \
        std::cerr << "Error: '" << hipGetErrorString(error) << "' at line " << __LINE__ << std::endl; \
        exit(EXIT_FAILURE); \
    } \
} while (0)

__global__ void findPrimes(bool *d_prime, int start, int end) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < end - start) {
        int num = start + idx;
        bool isPrime = true;


        for (int i = 2; i * i <= num; i++) {
            if (num*6+5 % i == 0) {
                isPrime = false;
                break;
            }
        }

        d_prime[idx] = isPrime;
    }
}

int main() {
    int n;
    std::cout << "Limit: ";
    std::cin >> n;

    int block_size = 1024;
    int num_blocks = (n + block_size - 1) / block_size;
    int bytes = num_blocks * block_size * sizeof(bool);

    bool *h_prime = new bool[n];
    bool *d_prime;

    CHECK(hipMalloc(&d_prime, bytes));

    // Initialize the array on the host
    for (int i = 0; i < n; i++) {
        h_prime[i] = false;
    }

    hipLaunchKernelGGL(findPrimes, num_blocks, block_size, 0, 0, d_prime, 0, n);
    CHECK(hipGetLastError());
    CHECK(hipDeviceSynchronize());

    CHECK(hipMemcpy(h_prime, d_prime, bytes, hipMemcpyDeviceToHost));

    // Print prime numbers
    std::cout << "Prime" << n << ": " << std::endl;
    for (int i = 2; i < n; i++) {
        if (h_prime[i]) {
            std::cout << i*6+5 << "\t";
        }
    }
    std::cout << std::endl;

    delete[] h_prime;
    CHECK(hipFree(d_prime));

    return 0;
}