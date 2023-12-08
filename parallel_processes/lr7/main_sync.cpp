#include<iostream>
#include<tuple>
#include<queue>
#include<ctime>

int const N = 8;
int const M = 8;
int const COUNT_STEPS = 8;
int const end_master_step = 3;

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
    int start_x = 1;
    int start_y = 1;
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

    if (current_step > end_master_step) {
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

    std::cout << "Start main" << std::endl;
    int start_x, start_y;
    bool custom_start = false;
    double start_time, finish_time;

    // init task
    Task initTask;     
    for(auto &subnumbers : initTask.desk)
        for(auto &number : subnumbers)
            number = 0;

    start_time = clock();
    master_step(start_x, start_y, 0, initTask.desk);
    Task newTask = MASTER_QUEUE.front();
    MASTER_QUEUE.pop();
    newTask = MASTER_QUEUE.front();
    MASTER_QUEUE.pop();

    TaskResult task_result = next_step(newTask.start_x, newTask.start_y, end_master_step, newTask.desk);
    if (task_result.result) {
        std::cout << "Solution found!" << std::endl;
        print_desk(task_result.desk);
    } else {
        std::cout << "Solution not found" << std::endl;
    }
    std::cout << std::endl;

    // while (!MASTER_QUEUE.empty()) {
    //     Task newTask = MASTER_QUEUE.front();
    //     std::cout << "Next task: " << newTask.start_x << "," << newTask.start_y << std::endl;
    //     // print_desk(newTask.desk);
    //     MASTER_QUEUE.pop();

    //     TaskResult task_result = next_step(newTask.start_x, newTask.start_y, end_master_step, newTask.desk);
    //     if (task_result.result) {
    //         std::cout << "Solution found!" << std::endl;
    //         print_desk(task_result.desk);
    //     } else {
    //         std::cout << "Solution not found" << std::endl;
    //     }
    //     std::cout << std::endl;
    // }
    finish_time = clock();

    double seconds = (finish_time - start_time) / CLOCKS_PER_SEC;
    std::cout << "Process time: " << seconds << " seconds" << std::endl;

    std::cout << "Finish main" << std::endl;
}


// параллельное решение:
// мастер доходит до глубины 3 (как пример) дальше ждет другие процессы Receive, получает их rank, и отправляет им поддерерво
// после окончания всех поддеревьев создает цикл по всем процессам и ожидает ответа окончания, принимает результат и отдает команду окончания работы
// сводит результаты в один и отдает результат пользователю
// другие процессы отправляют сигнал с текущим результатом и готовностью взять следующую работу, далее выполняют работу либо заканчивают
