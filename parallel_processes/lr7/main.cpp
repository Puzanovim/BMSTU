#include<iostream>
#include<ctime>
#include<tuple>
#include<queue>
#include <mpi.h>

int const N = 8;
int const M = 8;
int const COUNT_STEPS = 8;
int const DESK_SIZE = N * M;
int const MASTER_RANK = 0;
int const END_MASTER_STEP = 3;

# define EMPTY_REQUEST_TAG = 0;
# define TASK_RESPONSE_TAG = 10;
# define REQUEST_WITH_RESULT_TAG = 11;
# define STOP_WORK_TAG = -1;

int steps[COUNT_STEPS][2] = {
    {-2, 1},
    {-1, 2},
    {1, 2},
    {2, 1},
    {2, -1},
    {1, -2},
    {-1, -2},
    {-2, -1},
};

struct Task {
    int start_x = 0;
    int start_y = 0;
    int desk[N][M];
};


struct TaskResult {
    bool result = true;
    int desk[N][M];
};

std::queue<Task> MASTER_QUEUE;


void print_desk(int (&current_desk)[N][M]) {
    std::cout << std::endl;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            int value = current_desk[i][j];
            std::cout << " " << value << " ";
            if (value < 10)
                std::cout << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

Task create_new_task(int x, int y, int (&current_desk)[N][M]) {
    Task newTask = {x, y};
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < M; ++j)
            newTask.desk[i][j] = current_desk[i][j];

    return newTask;
}

TaskResult create_new_task_result(bool result, int (&current_desk)[N][M]) {
    TaskResult new_task_result = {result};
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < M; ++j)
            new_task_result.desk[i][j] = current_desk[i][j];

    return new_task_result;
}

bool master_step(int x, int y, int current_step, int (&current_desk)[N][M]) {
    if (x < 0 || x > N - 1 || y < 0 || y > M - 1)
        return false;

    if (current_desk[x][y] != 0) {
        return false;
    }
    
    current_step++;

    if (current_step > END_MASTER_STEP) {
        std::cout << "stop step: " << current_step << " x " << x << " y " << y << std::endl;
        Task currentTask = create_new_task(x, y, current_desk);
        MASTER_QUEUE.push(currentTask);
    } else {
        current_desk[x][y] = current_step;
        if (current_step == N * M)
            return true;
        
        for (int step = 0; step < COUNT_STEPS; ++step) {
            if (master_step(x + steps[step][0], y + steps[step][1], current_step, current_desk)) {
                return true;
            }
        }
    }

    // бэктрекинг
    current_step--;
    current_desk[x][y] = 0;
    return false;
}

TaskResult next_step(int x, int y, int current_step, int (&current_desk)[N][M]) {
    if (x < 0 || x > N - 1 || y < 0 || y > M - 1)
        return create_new_task_result(false, current_desk);

    if (current_desk[x][y] != 0) {
        return create_new_task_result(false, current_desk);
    }

    current_step++;
    current_desk[x][y] = current_step;
    if (current_step == N * M) {
        return create_new_task_result(true, current_desk);
    }
        
    for (int step = 0; step < COUNT_STEPS; ++step) {
        TaskResult next_result = next_step(x + steps[step][0], y + steps[step][1], current_step, current_desk);
        if (next_result.result) {
            return next_result;
        }
    }

    // бэктрекинг
    current_step--;
    current_desk[x][y] = 0;
    return create_new_task_result(false, current_desk);
}


int main(int argc, char **argv) {
    int rank, procs_count, len;
    double start_time, finish_time;
    MPI_Status status;
    char name[MPI_MAX_PROCESSOR_NAME];
    Task nextTask;
    TaskResult result;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &procs_count);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Get_processor_name(name, &len);

    if (rank == MASTER_RANK) {
        int results_count = 0, success_result_count = 0;
        TaskResult common_results[N * M];

        // init task
        Task initTask;     
        for(auto &subnumbers : initTask.desk)
            for(auto &number : subnumbers)
                number = 0;

        start_time = clock();

        // доходим до уровня 3
        master_step(start_x, start_y, 0, initTask.desk);

        // пока есть задания в очереди
        while (!MASTER_QUEUE.empty()) {    
            // получаем ранг свободного процесса
            MPI_Recv(result, DESK_SIZE, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);  // TODO указать тип результата
            auto sender_rank = status.MPI_SOURCE;
            auto sender_tag = status.MPI_TAG;

            // если есть какой-то результат, сохраняем его
            if (sender_tag == REQUEST_WITH_RESULT_TAG) {
                common_results[results_count] = result;
                results_count++;
            }
            
            // достаем следующее задание
            nextTask = MASTER_QUEUE.front();
            MASTER_QUEUE.pop();

            // отправляем задание процессу
            MPI_Send(nextTask, DESK_SIZE, MPI_INT, sender_rank, TASK_RESPONSE_TAG, MPI_COMM_WORLD);  // TODO отправить задание
        }

        for (int i = 0; i < procs_count; ++i) {
            // получаем номер освободившегося процесса и результат его работы
            MPI_Recv(result, DESK_SIZE, MPI_INT, i, MPI_ANY_TAG, MPI_COMM_WORLD, &status);  // TODO указать тип результата
            
            // если есть какой-то результат, сохраняем его
            if (sender_tag == REQUEST_WITH_RESULT_TAG) {
                common_results[results_count] = result;
                results_count++;
            }

            // отправляем команду на завершение работы
            MPI_Send(result, DESK_SIZE, MPI_INT, i, STOP_WORK_TAG, MPI_COMM_WORLD);  // TODO посмотреть насчет буфера и размера
        }
        finish_time = clock();

        for (int i = 0; i < results_count; ++i) {
            result = common_results[i];
            if (result.result) {
                print_desk(result.desk);
                success_result_count++;
            }
        }

        double seconds = (finish_time - start_time) / CLOCKS_PER_SEC;
        std::cout << "Process time: " << seconds << " seconds" << std::endl;
        
    } else {
        // отправляем сообщение о готовности мастеру
        MPI_Send(result, DESK_SIZE, MPI_INT, MASTER_RANK, EMPTY_REQUEST_TAG, MPI_COMM_WORLD);  // TODO указать тип результата

        while (True) {
            // получаем данные от мастера
            MPI_Recv(nextTask, DESK_SIZE, MPI_INT, MASTER_RANK, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            auto sender_tag = status.MPI_TAG;

            // смотрим на данные, если это задание, то делаем, если нет, то завершаем работу
            if (sender_tag == STOP_WORK_TAG)
                break;
            
            // выполняем задание
            result = next_step(nextTask.start_x, nextTask.start_y, END_MASTER_STEP, nextTask.desk);

            // отправляем результат мастеру
            MPI_Send(result, DESK_SIZE, MPI_INT, MASTER_RANK, REQUEST_WITH_RESULT_TAG, MPI_COMM_WORLD);  // TODO указать тип результата
        }
    }

    MPI_Finalize();
}