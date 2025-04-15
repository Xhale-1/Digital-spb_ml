package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type QueryRequest struct {
	Query string `json:"query"`
}

type QueryResponse struct {
	Response string `json:"response"`
}

func queryHandler(w http.ResponseWriter, r *http.Request) {

	//Получаем информацию из запроса
	fmt.Println("Request Method:", r.Method)
	fmt.Println("Request URL:", r.URL.String())

	body, _ := io.ReadAll(r.Body)
	defer r.Body.Close()
	fmt.Println("Request Body:", string(body))

	//парсим body в переменные
	var req QueryRequest
	json.Unmarshal(body, &req)

	// совершаем какие то операции//

	//преобразуем результат в json
	response := QueryResponse{
		Response: "You sent: " + req.Query,
	}

	//Заполняем заголовки
	w.Header().Set("Content-Type", "application/json")
	//Заполняем в http body энкодированный в json текст response
	json.NewEncoder(w).Encode(response)

}

func main() {
	http.HandleFunc("/api/process_query", queryHandler)
	http.ListenAndServe(":8080", nil)
}
