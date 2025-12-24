package async

import (
	"context"
	"fmt"
	"time"
)

// MergeChannels - объединить несколько каналов в один
func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
	out := make(chan int)

	go func() {
		defer close(out)
		for _, ch := range chs {
			for {
				select {
				case val, ok := <-ch:
					if !ok {
						goto nextChannel
					}
					select {
					case out <- val:
					case <-ctx.Done():
						return
					}
				case <-ctx.Done():
					return
				}
			}
			nextChannel:
		}
	}()

	return out
}

// BufferedChannelProcessor - обработать данные с буфером
func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
	output := make(chan int, bufferSize)

	go func() {
		defer close(output)
		for val := range input {
			output <- val * 2
		}
	}()

	return output
}

// DemoChannels - демонстрация работы с каналами
func DemoChannels() {
	fmt.Println("\n=== КАНАЛЫ И SELECT ===")

	ch := make(chan int, 3)

	go func() {
		defer close(ch)
		for i := 1; i <= 5; i++ {
			fmt.Printf(" Отправляем: %d\n", i)
			ch <- i
			time.Sleep(100 * time.Millisecond)
		}
	}()

	for {
		select {
		case val, ok := <-ch:
			if !ok {
				fmt.Println(" Канал закрыт")
				return
			}
			fmt.Printf(" Получили: %d\n", val)
		case <-time.After(500 * time.Millisecond):
			fmt.Println("  Таймаут!")
		}
	}
}

// DemoBuferizedChannel - демонстрация буферизованного канала
func DemoBuferizedChannel() {
	fmt.Println("\n=== БУФЕРИЗОВАННЫЙ КАНАЛ ===")

	input := make(chan int, 5)

	for i := 1; i <= 5; i++ {
		input <- i
	}
	close(input)

	output := BufferedChannelProcessor(input, 3)

	fmt.Println("Обработанные значения:")
	for val := range output {
		fmt.Printf("  %d\n", val)
	}
}
