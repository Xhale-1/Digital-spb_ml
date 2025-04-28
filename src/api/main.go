package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type QueryRequest struct {
	Query string `json:"query"`
}

type QueryResponse struct {
	Response []string `json:"response"`
}

// func queryHandler(w http.ResponseWriter, r *http.Request) {

// 	// Получаем информацию из запроса
// 	fmt.Println("Request Method:", r.Method)
// 	fmt.Println("Request URL:", r.URL.String())

// 	body, _ := io.ReadAll(r.Body)
// 	defer r.Body.Close()
// 	fmt.Println("Request Body:", string(body))

// 	// Создаем новый POST-запрос
// 	resp, err := http.Post("http://ai:8081/analyze", "application/json", bytes.NewReader(body))
// 	if err != nil {
// 		http.Error(w, "Failed to forward request: "+err.Error(), http.StatusInternalServerError)
// 		return
// 	}
// 	defer resp.Body.Close()

// 	// Читаем ответ от другого контейнера
// 	respBody, _ := io.ReadAll(resp.Body)

// 	// Возвращаем его назад клиенту
// 	w.Header().Set("Content-Type", "application/json")
// 	w.WriteHeader(resp.StatusCode)
// 	w.Write(respBody)

// }

// Структура запроса клиента
type ClientRequest struct {
	Query string `json:"query"`
}

// Структура запроса к ai/analyze
type AiAnalyzeRequest struct {
	Line string `json:"line"`
}

// Структура ответа от ai/analyze (массив словарей)
// type AiAnalyzeResponse []struct {
// 	Type  string `json:"type"`
// 	Value string `json:"value"`
// }

// Структура ответа от tree2/search_by_class
type Tree2Response struct {
	Response []string `json:"response"`
}

// Структура для внешнего ответа от AI
type AiRawResponse struct {
	Response string `json:"response"`
}

// Структура для одного элемента внутри массива
type AiAnalyzeItem struct {
	Type  int    `json:"type"` // Обрати внимание: type приходит как ЧИСЛО, а не строка
	Value string `json:"value"`
}

// Структура для массива элементов
type AiAnalyzeResponse []AiAnalyzeItem

func queryHandler(w http.ResponseWriter, r *http.Request) {
	// Получаем информацию из запроса
	fmt.Println("Request Method:", r.Method)
	fmt.Println("Request URL:", r.URL.String())
	// Проверяем возможность печати в консоль отмечая факт получения
	fmt.Println("Hello world!")
	// Читаем тело запроса
	body, err := io.ReadAll(r.Body)
	if err != nil {
		//Выводим ошибку в логи с помщью fmt.Println
		fmt.Println("Error reading request body:", err.Error())
		http.Error(w, "Failed to read body: "+err.Error(), http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	fmt.Println("Request Body:", string(body))

	// Парсим тело запроса клиента
	var clientReq ClientRequest
	if err := json.Unmarshal(body, &clientReq); err != nil {
		//Выводим ошибку в логи с помщью fmt.Println
		fmt.Println("Error parsing JSON:", err.Error())
		http.Error(w, "Failed to parse JSON: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Формируем новый запрос для ai/analyze
	aiReq := AiAnalyzeRequest{
		Line: clientReq.Query,
	}
	aiReqBody, err := json.Marshal(aiReq)
	if err != nil {
		//Выводим ошибку в логи с помщью fmt.Println
		fmt.Println("Error marshalling AI request JSON:", err.Error())
		http.Error(w, "Failed to marshal AI request JSON: "+err.Error(), http.StatusInternalServerError)
		return
	}

	// Отправляем запрос в контейнер ai
	resp, err := http.Post("http://ai:8081/analyze", "application/json", bytes.NewReader(aiReqBody))
	if err != nil {
		//Выводим ошибку в логи с помщью fmt.Println
		fmt.Println("Error posting to AI:", err.Error())
		http.Error(w, "Failed to forward to AI: "+err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Читаем ответ от ai
	aiRespBody, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading AI response:", err.Error())
		http.Error(w, "Failed to read AI response: "+err.Error(), http.StatusInternalServerError)
		return
	}

	// Шаг 1: сначала распарсим внешний объект
	var rawResp AiRawResponse
	if err := json.Unmarshal(aiRespBody, &rawResp); err != nil {
		fmt.Println("Error parsing AI raw response JSON:", err.Error())
		http.Error(w, "Failed to parse AI raw response JSON: "+err.Error(), http.StatusInternalServerError)
		return
	}

	// Шаг 2: теперь распарсим строку внутри поля "response" в массив объектов
	var aiResp AiAnalyzeResponse
	if err := json.Unmarshal([]byte(rawResp.Response), &aiResp); err != nil {
		fmt.Println("Error parsing AI inner response JSON:", err.Error())
		http.Error(w, "Failed to parse AI inner response JSON: "+err.Error(), http.StatusInternalServerError)
		return
	}

	// Пересылаем ответ от ai в tree2/search_by_class
	treeResp, err := forwardToTree2(aiResp)
	if err != nil {
		//Выводим ошибку в логи с помщью fmt.Println
		fmt.Println("Error forwarding to Tree2:", err.Error())
		http.Error(w, "Failed to forward to Tree2: "+err.Error(), http.StatusInternalServerError)
		return
	}

	// Возвращаем ответ клиенту
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(treeResp)
}

// Отдельная функция отправки запроса в tree2/search_by_class
func forwardToTree2(aiData AiAnalyzeResponse) (*Tree2Response, error) {
	// Сериализуем ответ от ai в JSON
	payload, err := json.Marshal(aiData)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal AI data: %w", err)
	}

	// Отправляем POST запрос на tree2
	// Здесь предполагается, что tree2 принимает JSON в том же формате, что и ai/analyze
	// Факт отправки запроса отмечается влогах с помощью fmt.Println
	fmt.Println("Forwarding to Tree2:", string(payload))

	resp, err := http.Post("http://tree2:5000/search_by_class", "application/json", bytes.NewReader(payload))
	if err != nil {
		// Выводим ошибку в логи с помощью fmt.Println
		fmt.Println("Error posting to Tree2:", err)
		// Возвращаем ошибку, если не удалось отправить запрос
		return nil, fmt.Errorf("failed to post to Tree2: %w", err)
	}
	defer resp.Body.Close()

	// Читаем ответ от tree2
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read Tree2 response: %w", err)
	}

	// Парсим JSON ответа
	var treeResp Tree2Response
	if err := json.Unmarshal(respBody, &treeResp); err != nil {
		return nil, fmt.Errorf("failed to parse Tree2 JSON: %w", err)
	}

	return &treeResp, nil
}

func main() {
	http.HandleFunc("/api/query", queryHandler)
	http.ListenAndServe(":8080", nil)
}
