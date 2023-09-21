#!/bin/bash

model="tiiuae/falcon-180B-chat"
number_of_gpus="8"
host="127.0.0.1"
port="8000"
PID=$$


while getopts ":m:n:a:p:" opt; do
  case $opt in
    m) model="$OPTARG"
    ;;
    n) number_of_gpus="$OPTARG"
    ;;
    a) host="$OPTARG"
    ;;
    p) port="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) echo "Option $opt needs a valid argument"
    exit 1
    ;;
  esac
done

IFS="/"
read -ra ADDR <<< $model
modelname=${ADDR[1]}
IFS=""  # reset IFS

nohup /root/miniconda3/envs/LLM/bin/python -m vllm.entrypoints.openai.api_server \
--host ${host} \
--port ${port} \
--model ${model} \
--tensor-parallel-size ${number_of_gpus} > "logs/serving_${modelname}.log" &

echo $! > "logs/pid_file"