package async

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// Task - задача для обработки
type Task struct {
	ID   int
	Data interface{}
}

// Result - результат обработки
type Result struct {
	TaskID int
	Output interface{}
	Error  error
}

// WorkerPool - пул воркеров
type WorkerPool struct {
	workersCount int
	tasks        chan Task
	results      chan Result
	wg           sync.WaitGroup
	resultWg     sync.WaitGroup
}

// NewWorkerPool - создать новый пул воркеров
func NewWorkerPool(workers int) *WorkerPool {
	return &WorkerPool{
		workersCount: workers,
		tasks:        make(chan Task, workers*2),
		results:      make(chan Result, workers*2),
	}
}

// Start - запустить воркеры
func (wp *WorkerPool) Start(ctx context.Context, processor func(Task) Result) {
	for i := 0; i < wp.workersCount; i++ {
		wp.wg.Add(1)
		go func(workerID int) {
			defer wp.wg.Done()
			fmt.Printf(" Воркер %d запущен\n", workerID)

			for {
				select {
				case task, ok := <-wp.tasks:
					if !ok {
						fmt.Printf(" Воркер %d завершен\n", workerID)
						return
					}
					fmt.Printf(" Воркер %d обрабатывает задачу %d\n", workerID, task.ID)
					result := processor(task)

					select {
					case wp.results <- result:
						wp.resultWg.Done()
					case <-ctx.Done():
						return
					}
				case <-ctx.Done():
					fmt.Printf(" Воркер %d отменен\n", workerID)
					return
				}
			}
		}(i)
	}
}

// Submit - отправить задачу
func (wp *WorkerPool) Submit(task Task) {
	wp.resultWg.Add(1)
	wp.tasks <- task
}

// GetResults - получить канал результатов
func (wp *WorkerPool) GetResults() <-chan Result {
	return wp.results
}

// Stop - остановить пул
func (wp *WorkerPool) Stop() {
	close(wp.tasks)
	wp.wg.Wait()
	wp.resultWg.Wait()
	close(wp.results)
}

// ProcessTasks - обработать список задач
func (wp *WorkerPool) ProcessTasks(ctx context.Context, tasks []Task, processor func(Task) Result) []Result {
	go wp.Start(ctx, processor)

	for _, task := range tasks {
		wp.Submit(task)
	}

	wp.Stop()

	var results []Result
	for result := range wp.results {
		results = append(results, result)
	}

	return results
}

// DemoWorkerPool - демонстрация Worker Pool
func DemoWorkerPool() {
	fmt.Println("\n=== WORKER POOL ===")

	pool := NewWorkerPool(3)
	ctx := context.Background()

	tasks := []Task{
		{ID: 1, Data: 10},
		{ID: 2, Data: 20},
		{ID: 3, Data: 30},
		{ID: 4, Data: 40},
		{ID: 5, Data: 50},
	}

	processor := func(task Task) Result {
		time.Sleep(500 * time.Millisecond)
		value := task.Data.(int)
		return Result{
			TaskID: task.ID,
			Output: value * 2,
		}
	}

	results := pool.ProcessTasks(ctx, tasks, processor)

	fmt.Println("\n Результаты обработки:")
	for _, result := range results {
		fmt.Printf("  Задача %d: %v\n", result.TaskID, result.Output)
	}
}
