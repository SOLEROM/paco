# run in docker


docker build -t ollama-llama3.2 .

docker run -d --name ollama3 -p 11434:11434 ollama-llama3.2

docker exec -it ollama3 ollama run llama3.2