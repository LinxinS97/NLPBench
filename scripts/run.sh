DIR=/home/elpis_ubuntu/LLM/NLPBench


# zero-shot, cot, sys, cot + sys
# python $DIR/run.py with "configs/zero-shot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
# wait

# python $DIR/run.py with "configs/zero-shot.yaml" "model_name='gpt-4'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='gpt-4'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='gpt-4'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='gpt-4'" "ctx=False"
# wait

# python $DIR/run.py with "configs/zero-shot.yaml" "model_name='models/text-bison-001'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_sys.yaml" "model_name='models/text-bison-001'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_cot.yaml" "model_name='models/text-bison-001'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_sys_cot.yaml" "model_name='models/text-bison-001'" "ctx=False"
# wait


# few-shot, cot, sys, cot + sys
#python $DIR/run.py with "configs/few-shot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait

#python $DIR/run.py with "configs/few-shot.yaml" "model_name='gpt-4'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='gpt-4'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='gpt-4'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='gpt-4'" "ctx=False"
#wait

#python $DIR/run.py with "configs/few-shot.yaml" "model_name='models/text-bison-001'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys.yaml" "model_name='models/text-bison-001'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_cot.yaml" "model_name='models/text-bison-001'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sys_cot.yaml" "model_name='models/text-bison-001'" "ctx=False"
#wait

# zero-shot, tot
# python $DIR/run.py with "configs/zero-shot_tot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_tot.yaml" "model_name='gpt-4'" "ctx=False"
# wait
# python $DIR/run.py with "configs/zero-shot_tot.yaml" "model_name='models/text-bison-001'" "ctx=False"
# wait

# few-shot, tot
# python $DIR/run.py with "configs/few-shot_tot.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
# wait
# python $DIR/run.py with "configs/few-shot_tot.yaml" "model_name='gpt-4'" "ctx=False"
# wait
# python $DIR/run.py with "configs/few-shot_tot.yaml" "model_name='models/text-bison-001'" "ctx=False"
# wait

# zero-shot, self consistency
#python $DIR/run.py with "configs/zero-shot_sc.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait
#python $DIR/run.py with "configs/zero-shot_cot_sc.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait
#python $DIR/run.py with "configs/zero-shot_sc.yaml" "model_name='gpt-4'" "ctx=False"
#wait
#python $DIR/run.py with "configs/zero-shot_cot_sc.yaml" "model_name='gpt-4'" "ctx=False"
#wait
#python $DIR/run.py with "configs/zero-shot_sc.yaml" "model_name='models/text-bison-001'" "ctx=False"
#wait
#python $DIR/run.py with "configs/zero-shot_cot_sc.yaml" "model_name='models/text-bison-001'" "ctx=False"
#wait

# few-shot, self consistency
#python $DIR/run.py with "configs/few-shot_sc.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_cot_sc.yaml" "model_name='gpt-3.5-turbo'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sc.yaml" "model_name='gpt-4'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_cot_sc.yaml" "model_name='gpt-4'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_sc.yaml" "model_name='models/text-bison-001'" "ctx=False"
#wait
#python $DIR/run.py with "configs/few-shot_cot_sc.yaml" "model_name='models/text-bison-001'" "ctx=False"