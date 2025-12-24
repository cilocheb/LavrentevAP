package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"sync"
	"sync/atomic"
	"time"
)

// Server - многопоточный HTTP сервер
type Server struct {
	router       *http.ServeMux
	requestCount int64
	server       *http.Server
	mu           sync.Mutex
}

// NewServer - создать новый сервер
func NewServer(addr string) *Server {
	s := &Server{
		router: http.NewServeMux(),
	}

	s.setupRoutes()

	s.server = &http.Server{
		Addr:    addr,
		Handler: s.router,
	}

	return s
}

// setupRoutes - настроить маршруты
func (s *Server) setupRoutes() {
	s.router.HandleFunc("/", s.handleRoot)
	s.router.HandleFunc("/health", s.handleHealth)
	s.router.HandleFunc("/stats", s.handleStats)
}

// handleRoot - обработчик корневого маршрута
func (s *Server) handleRoot(w http.ResponseWriter, r *http.Request) {
	count := atomic.AddInt64(&s.requestCount, 1)
	time.Sleep(50 * time.Millisecond)
	fmt.Fprintf(w, "Hello! Request count: %d\n", count)
	log.Printf(" Обработан запрос #%d", count)
}

// handleHealth - обработчик проверки здоровья
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}

// handleStats - обработчик статистики
func (s *Server) handleStats(w http.ResponseWriter, r *http.Request) {
	count := atomic.LoadInt64(&s.requestCount)
	fmt.Fprintf(w, "Total requests: %d", count)
}

// Start - запустить сервер
func (s *Server) Start() error {
	log.Printf(" Сервер запущен на %s", s.server.Addr)
	return s.server.ListenAndServe()
}

// Stop - остановить сервер
func (s *Server) Stop(ctx context.Context) error {
	log.Println(" Завершение работы сервера...")
	return s.server.Shutdown(ctx)
}

// GetRequestCount - получить количество запросов
func (s *Server) GetRequestCount() int64 {
	return atomic.LoadInt64(&s.requestCount)
}
