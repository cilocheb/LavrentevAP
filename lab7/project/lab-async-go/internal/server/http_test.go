package server

import (
	"context"
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// TestServer_Routes - тестирование маршрутов
func TestServer_Routes(t *testing.T) {
	server := NewServer(":0")

	tests := []struct {
		name       string
		path       string
		wantStatus int
	}{
		{
			name:       "root path",
			path:       "/",
			wantStatus: http.StatusOK,
		},
		{
			name:       "health check",
			path:       "/health",
			wantStatus: http.StatusOK,
		},
		{
			name:       "stats",
			path:       "/stats",
			wantStatus: http.StatusOK,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest("GET", tt.path, nil)
			w := httptest.NewRecorder()

			server.router.ServeHTTP(w, req)

			resp := w.Result()

			if resp.StatusCode != tt.wantStatus {
				t.Errorf("Expected status %d, got %d", tt.wantStatus, resp.StatusCode)
			}

			defer resp.Body.Close()
			body, _ := io.ReadAll(resp.Body)
			if len(body) == 0 {
				t.Error("Expected response body")
			}
		})
	}
}

// TestServer_ConcurrentRequests - тестирование конкурентных запросов
func TestServer_ConcurrentRequests(t *testing.T) {
	server := NewServer(":0")

	var wg sync.WaitGroup
	numGoroutines := 100

	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()

			req := httptest.NewRequest("GET", "/", nil)
			w := httptest.NewRecorder()

			server.router.ServeHTTP(w, req)

			if w.Code != http.StatusOK {
				t.Errorf("Expected status 200, got %d", w.Code)
			}
		}()
	}

	wg.Wait()

	if server.GetRequestCount() != int64(numGoroutines) {
		t.Errorf("Expected %d requests, got %d", numGoroutines, server.GetRequestCount())
	}
}

// TestServer_RequestCounter - тестирование счётчика запросов
func TestServer_RequestCounter(t *testing.T) {
	server := NewServer(":0")

	for i := 0; i < 5; i++ {
		req := httptest.NewRequest("GET", "/", nil)
		w := httptest.NewRecorder()
		server.router.ServeHTTP(w, req)
	}

	count := server.GetRequestCount()
	if count != 5 {
		t.Errorf("Expected 5 requests, got %d", count)
	}
}

// TestServer_HealthCheck - тестирование проверки здоровья
func TestServer_HealthCheck(t *testing.T) {
	server := NewServer(":0")

	req := httptest.NewRequest("GET", "/health", nil)
	w := httptest.NewRecorder()

	server.router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	defer w.Result().Body.Close()
	body, _ := io.ReadAll(w.Result().Body)
	if string(body) != "OK" {
		t.Errorf("Expected 'OK', got %s", string(body))
	}
}

// TestServer_Shutdown - тестирование корректного завершения
func TestServer_Shutdown(t *testing.T) {
	server := NewServer(":0")

	go server.Start()

	time.Sleep(100 * time.Millisecond)

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	err := server.Stop(ctx)
	if err != nil && err != http.ErrServerClosed {
		t.Errorf("Unexpected error during shutdown: %v", err)
	}
}

// BenchmarkServerThroughput - бенчмарк производительности сервера
func BenchmarkServerThroughput(b *testing.B) {
	server := NewServer(":0")

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			req := httptest.NewRequest("GET", "/", nil)
			w := httptest.NewRecorder()
			server.router.ServeHTTP(w, req)
		}
	})
}
