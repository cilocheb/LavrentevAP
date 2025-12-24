package async

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// Producer - создать канал с данными
func Producer(ctx context.Context, id int, count int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < count; i++ {
			select {
			case out <- i:
				fmt.Printf(" Продюсер %d: %d\n", id, i)
			case <-ctx.Done():
				fmt.Printf(" Продюсер %d отменен\n", id)
				return
			}
			time.Sleep(100 * time.Millisecond)
		}
	}()
	return out
}

// Worker - обработать данные
func Worker(ctx context.Context, in <-chan int, id int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			select {
			case out <- n * n:
				fmt.Printf(" Воркер %d обработал %d → %d\n", id, n, n*n)
			case <-ctx.Done():
				fmt.Printf(" Воркер %d отменен\n", id)
				return
			}
			time.Sleep(50 * time.Millisecond)
		}
	}()
	return out
}

// Merge - объединить результаты (Fan-In)
func Merge(ctx context.Context, inputs ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)

	output := func(c <-chan int) {
		defer wg.Done()
		for n := range c {
			select {
			case out <- n:
			case <-ctx.Done():
				return
			}
		}
	}

	wg.Add(len(inputs))
	for _, input := range inputs {
		go output(input)
	}

	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

// DemoFanOutFanIn - демонстрация Fan-Out/Fan-In паттерна
func DemoFanOutFanIn() {
	fmt.Println("\n=== FAN-OUT / FAN-IN ===")

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	// Fan-Out: несколько продюсеров
	p1 := Producer(ctx, 1, 3)
	p2 := Producer(ctx, 2, 3)

	// Worker pool
	w1 := Worker(ctx, p1, 1)
	w2 := Worker(ctx, p2, 2)

	// Fan-In: объединение результатов
	results := Merge(ctx, w1, w2)

	fmt.Println("\n Итоговые результаты:")
	for result := range results {
		fmt.Printf("   %d\n", result)
	}
}
