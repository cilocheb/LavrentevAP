package async

import (
	"fmt"
	"sync"
	"time"
)

// Counter - безопасный счётчик для конкурентного доступа
type Counter struct {
	mu    sync.Mutex
	value int
}

// Increment - увеличить счётчик на 1
func (c *Counter) Increment() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

// Value - получить текущее значение
func (c *Counter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// ProcessItems - обработать элементы параллельно
func ProcessItems(items []int, processor func(int)) {
	var wg sync.WaitGroup

	for _, item := range items {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			processor(i)
			time.Sleep(10 * time.Millisecond)
		}(item)
	}

	wg.Wait()
}

// DemoBasicGoroutines - демонстрация базовых горутин
func DemoBasicGoroutines() {
	fmt.Println("\n=== БАЗОВЫЕ ГОРУТИНЫ И WAITGROUP ===")

	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			fmt.Printf(" Горутина %d запущена\n", id)
			time.Sleep(time.Second)
			fmt.Printf(" Горутина %d завершена\n", id)
		}(i)
	}

	wg.Wait()
	fmt.Println(" Все горутины завершены")
}

// DemoCounter - демонстрация потокобезопасного счётчика
func DemoCounter() {
	fmt.Println("\n=== ПОТОКОБЕЗОПАСНЫЙ СЧЁТЧИК ===")

	counter := &Counter{}
	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}

	wg.Wait()

	fmt.Printf(" Финальное значение счётчика: %d (ожидается 100)\n", counter.Value())
}
