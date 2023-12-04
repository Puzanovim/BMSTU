#include<iostream>
#include<ctime>
#include <mpi.h>

int const N = 8;
int const M = 8;
int const count_steps = 8;

int desk[N][M];
int steps[count_steps][2] = {
    {-2, 1},
    {-1, 2},
    {1, 2},
    {2, 1},
    {2, -1},
    {1, -2},
    {-1, -2},
    {-2, -1},
};

void init_desk() {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            desk[i][j] = 0;
        }
    }
}

void print_desk() {
    std::cout << std::endl;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            int value = desk[i][j];
            std::cout << " " << value << " ";
            if (value < 10)
                std::cout << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

bool next_step(int x, int y, int current_step) {
    if (x < 0 || x > N - 1 || y < 0 || y > M - 1)
        return false;

    if (desk[x][y] != 0) {
        return false;
    }
    
    current_step++;
    desk[x][y] = current_step;
    if (current_step == N * M)
        return true;

    for (int step = 0; step < count_steps; ++step) {
        if (next_step(x + steps[step][0], y + steps[step][1], current_step)) {
            return true;
        }
    }
    
    current_step--;
    desk[x][y] = 0;
    return false;
}

int main(int argc, char **argv) {

    int start_x, start_y, rank, procs_count, len;
    bool custom_start = false;
    double start_time, finish_time;
    char name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &procs_count);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(name, &len);

    init_desk();

    if (custom_start)
        std::cin >> start_x >> start_y;
    else {
        start_x = 0;
        start_y = 0;
    }

    start_time = clock();
    next_step(start_x, start_y, 0);
    finish_time = clock();

    print_desk();
    double seconds = (finish_time - start_time) / CLOCKS_PER_SEC;
    std::cout << "Process time: " << seconds << " seconds" << std::endl;

    MPI_Finalize();
}