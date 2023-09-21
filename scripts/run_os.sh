PID_file="logs/pid_file"
DIR=/root/llm/NLPBench

getpid() {
    head -1 < $PID_file
}


#nohup bash $DIR/scripts/serving.sh -m "meta-llama/Llama-2-13b-chat-hf" 2>&1
#sleep 90
#PID=$(getpid)
# python $DIR/run.py with "configs/zero-shot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
# wait
#python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=False"
#wait

#python $DIR/run.py with "configs/zero-shot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=true"
#wait
#python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=true"
#wait
#python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=true"
#wait
#python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='meta-llama/Llama-2-13b-chat-hf'" "ctx=true"
#wait
#kill -9 $PID

nohup bash $DIR/scripts/serving.sh -m "meta-llama/Llama-2-70b-chat-hf" 2>&1
sleep 120
PID=$(getpid)
#python $DIR/run.py with "configs/zero-shot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
#wait
#python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
#wait
#python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
#wait
python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=False"
wait

python $DIR/run.py with "configs/zero-shot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='meta-llama/Llama-2-70b-chat-hf'" "ctx=True"
wait
kill -9 $PID

nohup bash $DIR/scripts/serving.sh -m "sambanovasystems/BLOOMChat-176B-v1" 2>&1
sleep 300
PID=$(getpid)
python $DIR/run.py with "configs/zero-shot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait
python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait
python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait
python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait
python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=False"
wait

python $DIR/run.py with "configs/zero-shot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='sambanovasystems/BLOOMChat-176B-v1'" "ctx=True"
wait
kill -9 $PID

