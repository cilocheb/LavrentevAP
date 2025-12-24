package main

import (
	"fmt"
	"lab-async-go/internal/async"
	"time"
)

func main() {

	fmt.Println("ЛАБОРАТОРНАЯ РАБОТА №7: АСИНХРОННОЕ ПРОГРАММИРОВАНИЕ В GO")


	// 1. Базовые горутины
	async.DemoBasicGoroutines()
	time.Sleep(2 * time.Second)

	// 2. Потокобезопасный счётчик
	async.DemoCounter()
	time.Sleep(1 * time.Second)

	// 3. Каналы и Select
	async.DemoChannels()
	time.Sleep(1 * time.Second)

	// 4. Буферизованный канал
	async.DemoBuferizedChannel()
	time.Sleep(1 * time.Second)

	// 5. Worker Pool
	async.DemoWorkerPool()
	time.Sleep(3 * time.Second)

	// 6. Fan-Out/Fan-In
	async.DemoFanOutFanIn()


	fmt.Println("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")

}
