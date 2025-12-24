package async

import (
	"context"
	"sync"
	"testing"
	"time"
)

func TestBasicGoroutines(t *testing.T) {
	var wg sync.WaitGroup
	results := make([]int, 5)

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			results[id] = id * 2
		}(i)
	}

	done := make(chan struct{})
	go func() {
		wg.Wait()
		close(done)
	}()

	select {
	case <-done:
		// Успешно
	case <-time.After(5 * time.Second):
		t.Fatal("Тест зависл (таймаут)")
	}

	for i := 0; i < 5; i++ {
		if results[i] != i*2 {
			t.Errorf("Ошибка в результате: ожидается %d, получено %d", i*2, results[i])
		}
	}
}

func TestThreadSafeCounter(t *testing.T) {
	var counter int
	var mu sync.Mutex
	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			mu.Lock()
			counter++
			mu.Unlock()
		}()
	}

	done := make(chan struct{})
	go func() {
		wg.Wait()
		close(done)
	}()

	select {
	case <-done:
		// Успешно
	case <-time.After(5 * time.Second):
		t.Fatal("Тест зависл (таймаут)")
	}

	if counter != 100 {
		t.Errorf("Ошибка счётчика: ожидается 100, получено %d", counter)
	}
}

func TestChannels(t *testing.T) {
	ch := make(chan int, 5)

	done := make(chan struct{})
	go func() {
		for i := 1; i <= 5; i++ {
			ch <- i
		}
		close(ch)
		close(done)
	}()

	select {
	case <-done:
		// Успешно
	case <-time.After(5 * time.Second):
		t.Fatal("Тест зависл (таймаут)")
	}

	count := 0
	for range ch {
		count++
	}

	if count != 5 {
		t.Errorf("Ошибка канала: ожидается 5 значений, получено %d", count)
	}
}

func TestWorkerPool(t *testing.T) {
	pool := NewWorkerPool(2)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	tasks := []Task{
		{ID: 1, Data: 10},
		{ID: 2, Data: 20},
	}

	processor := func(task Task) Result {
		value := task.Data.(int)
		return Result{
			TaskID: task.ID,
			Output: value * 2,
		}
	}

	results := pool.ProcessTasks(ctx, tasks, processor)

	if len(results) != len(tasks) {
		t.Errorf("Ошибка результатов: ожидается %d, получено %d", len(tasks), len(results))
	}
}

func TestFanOutFanIn(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	done := make(chan struct{})
	go func() {
		DemoFanOutFanIn()
		close(done)
	}()

	select {
	case <-done:
		// Успешно
	case <-ctx.Done():
		t.Fatal("Тест зависл (таймаут)")
	}
}

