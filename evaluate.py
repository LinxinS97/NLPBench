import json
import numpy as np
from os import listdir
from os.path import isfile, join

from utils import ApiManager

cates = [
    "Language Modeling and Syntax and Parsing",
    "Pragmatics and Discourse and Dialogue and Applications",
    "Semantics and Logic",
    "Information Retrieval and Topic Modeling",
    "Artificial Intelligence",
    "Other Topics"
]


class Evaluation:
    def __init__(self, seed, open_sourced):
        self.open_sourced = open_sourced
        self.seed = seed
        osd = '_os' if open_sourced else ''
        self.osd = osd

        self.no_ctx_files = [f for f in listdir(f'res/{seed}{osd}/no_ctx/') if
                             isfile(join(f'res/{seed}{osd}/no_ctx/', f))]
        self.ctx_files = [f for f in listdir(f'res/{seed}{osd}/ctx/') if isfile(join(f'res/{seed}{osd}/ctx/', f))]
        self.ctx_data = json.load(open('data/w_ctx.json', 'r'))
        self.no_ctx_data = json.load(open('data/wo_ctx.json', 'r'))

    def _init_result(self):
        return {
            'gpt-3.5-turbo': {},
            'gpt-4': {},
            'text-bison-001': {}
        } if self.open_sourced is False else {
            'Llama-2-70b-chat-hf': {},
            'Llama-2-13b-chat-hf': {},
        }

    def _file_format(self, f, ctx_path='no_ctx'):
        args = f.split('_')
        llm_name = f.split('_')[1].replace('.json', '')
        shot_type = f.split('_')[0]
        prompt_r = ''
        if len(args) == 3:
            prompt_r = f.split('_')[2].split('.')[0]
        if len(args) == 4:
            prompt_r = f.split('_')[2] + '_' + f.split('_')[3].split('.')[0]
        llm_res = json.load(open(f'res/{self.seed}{self.osd}/{ctx_path}/{f}', 'r'))
        if prompt_r != '':
            prompt_r = '_' + prompt_r

        return llm_name, shot_type, prompt_r, llm_res

    def _path_format(self, suffix):
        no_ctx_save_path = f'res/{self.seed}{self.osd}/res_no_ctx_{suffix}.json'
        ctx_save_path = f'res/{self.seed}{self.osd}/res_ctx_{suffix}.json'

        return no_ctx_save_path, ctx_save_path

    # We use accuracy to evaluate multiple choice questions
    def evaluate_mc(self):
        ### w/o context
        res = self._init_result()
        no_ctx_save_path, ctx_save_path = self._path_format('mc')

        for f in self.no_ctx_files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f)
            corr = {c: 0 for c in cates}
            cnt = {c: 0 for c in cates}
            for i, d in enumerate(llm_res):
                if d['type'] == 0:
                    cate = self.no_ctx_data[i]['category']
                    cate_cnt = cnt.get(cate, 0)
                    cnt[cate] = cate_cnt + 1
                    if d['retrived_answer'] is not None:
                        ans = set(d['answer'])
                        llm_ans = d['retrived_answer'].replace(' ', '').replace("'", '').replace('"', '').split(',')
                        try:
                            llm_ans = [int(a) for a in llm_ans]
                        except Exception:
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans
                        llm_ans = set(llm_ans)
                        if ans == llm_ans:
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans + 1
                        else:
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans

            acc = {k: v / cnt[k] if cnt[k] != 0 else 1 for k, v in corr.items()}
            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            overall_acc = np.sum(np.array(list(acc.values())) * np.array(list(cnt.values()))) / sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'acc': acc,
                'overall_acc': overall_acc
            }
        json.dump(res, open(no_ctx_save_path, 'w'), indent=4)

        ### w/ context
        res = self._init_result()
        for f in self.ctx_files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f, 'ctx')
            corr = {c: 0 for c in cates}
            cnt = {c: 0 for c in cates}
            for i, ds in enumerate(llm_res):
                for j, d in enumerate(ds['questions']):
                    if ds['type'][j] == 0:
                        cate = self.ctx_data[i]['category'][j]
                        cate_cnt = cnt.get(cate, 0)
                        cnt[cate] = cate_cnt + 1
                        if ds['retrived_answer'][j] is not None:
                            ans = set(ds['answers'][j])
                            llm_ans = ds['retrived_answer'][j].replace(' ', '').replace("'", '').replace('"', '').split(
                                ',')
                            try:
                                llm_ans = [int(a) for a in llm_ans]
                            except Exception:
                                cate_ans = corr.get(cate, 0)
                                corr[cate] = cate_ans
                                continue
                            llm_ans = set(llm_ans)
                            if ans == llm_ans:
                                cate_ans = corr.get(cate, 0)
                                corr[cate] = cate_ans + 1
                            else:
                                cate_ans = corr.get(cate, 0)
                                corr[cate] = cate_ans

            acc = {k: v / cnt[k] if cnt[k] != 0 else 1 for k, v in corr.items()}
            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            overall_acc = np.sum(np.array(list(acc.values())) * np.array(list(cnt.values()))) / sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'acc': acc,
                'overall_acc': overall_acc
            }
        json.dump(res, open(ctx_save_path, 'w'), indent=4)

    def evaluate_sc(self):
        ### w/o context
        res = self._init_result()
        no_ctx_save_path, ctx_save_path = self._path_format('mc-sc')
        files = [
            'few-shot-sc_gpt-3.5-turbo.json',
            'few-shot-sc_gpt-3.5-turbo_cot.json',
            'few-shot-sc_gpt-4.json',
            'few-shot-sc_gpt-4_cot.json',
            'few-shot-sc_text-bison-001.json',
            'few-shot-sc_text-bison-001_cot.json',
            'zero-shot-sc_gpt-3.5-turbo.json',
            'zero-shot-sc_gpt-3.5-turbo_cot.json',
            'zero-shot-sc_gpt-4.json',
            'zero-shot-sc_gpt-4_cot.json',
            'zero-shot-sc_text-bison-001.json',
            'zero-shot-sc_text-bison-001_cot.json',
        ]
        for f in files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f)
            corr = {c: 0 for c in cates}
            cnt = {c: 0 for c in cates}
            for i, d in enumerate(llm_res):
                if d['type'] == 0:
                    cate = self.no_ctx_data[i]['category']
                    cate_cnt = cnt.get(cate, 0)
                    cnt[cate] = cate_cnt + 1
                    if d['llm_answer'] is not None:
                        ans = set(d['answer'])
                        llm_ans = d['llm_answer'].replace(' ', '').replace("'", '').replace('"', '').split(',')
                        try:
                            llm_ans = [int(a) for a in llm_ans]
                        except Exception:
                            print('model:', f, '\nerr: ', llm_ans)
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans
                        llm_ans = set(llm_ans)
                        if ans == llm_ans:
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans + 1
                        else:
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans

            acc = {k: v / cnt[k] if cnt[k] != 0 else 1 for k, v in corr.items()}
            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            overall_acc = np.sum(np.array(list(acc.values())) * np.array(list(cnt.values()))) / sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'acc': acc,
                'overall_acc': overall_acc
            }
        json.dump(res, open(no_ctx_save_path, 'w'), indent=4)

        ### w/ context
        res = self._init_result()
        for f in files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f, 'ctx')
            corr = {c: 0 for c in cates}
            cnt = {c: 0 for c in cates}
            for i, ds in enumerate(llm_res):
                for j, d in enumerate(ds['questions']):
                    if ds['type'][j] == 0:
                        cate = self.ctx_data[i]['category'][j]
                        cate_cnt = cnt.get(cate, 0)
                        cnt[cate] = cate_cnt + 1
                        if ds['llm_answer'][j] is not None:
                            ans = set(ds['answers'][j])
                            llm_ans = ds['llm_answer'][j].replace(' ', '').replace("'", '').replace('"', '').split(
                                ',')
                            try:
                                llm_ans = [int(a) for a in llm_ans]
                            except Exception:
                                print('model:', f, '\nerr: ', llm_ans)
                                cate_ans = corr.get(cate, 0)
                                corr[cate] = cate_ans
                                continue
                            llm_ans = set(llm_ans)
                            if ans == llm_ans:
                                cate_ans = corr.get(cate, 0)
                                corr[cate] = cate_ans + 1
                            else:
                                cate_ans = corr.get(cate, 0)
                                corr[cate] = cate_ans

            acc = {k: v / cnt[k] if cnt[k] != 0 else 1 for k, v in corr.items()}
            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            overall_acc = np.sum(np.array(list(acc.values())) * np.array(list(cnt.values()))) / sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'acc': acc,
                'overall_acc': overall_acc
            }
        json.dump(res, open(ctx_save_path, 'w'), indent=4)

    # We use ROUGE-L, CIDEr (for unique answer) to evaluate short answer questions with unique answer
    def evaluate_sa_unique(self):
        from pycocoevalcap.rouge.rouge import Rouge
        from pycocoevalcap.cider.cider import Cider

        res = self._init_result()
        no_ctx_save_path, ctx_save_path = self._path_format('sa_unique')

        for f in self.no_ctx_files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f)

            llm_ans_dict = {}
            ans_dict = {}
            overall_llm_ans = {}
            overall_ans = {}
            cnt = {}
            for i, d in enumerate(llm_res):
                if d['type'] == 1 and self.no_ctx_data[i].get('unique_ans', None) == 1:
                    cate = self.no_ctx_data[i]['category']
                    cate_cnt = cnt.get(cate, 0)
                    cnt[cate] = cate_cnt + 1

                    ans = d['answer']
                    llm_ans = d['llm_answer']

                    if llm_ans == "" or llm_ans is None:
                        llm_ans = "No answer provided."

                    tmp1 = llm_ans_dict.get(cate, {})
                    tmp1[i] = [llm_ans]
                    llm_ans_dict[cate] = tmp1

                    tmp2 = ans_dict.get(cate, {})
                    tmp2[i] = [ans]
                    ans_dict[cate] = tmp2

                    overall_llm_ans[i] = [llm_ans]
                    overall_ans[i] = [ans]

            scores = {}
            for k in cnt.keys():
                rouge = Rouge().compute_score(llm_ans_dict[k], ans_dict[k])[0]
                cider = Cider().compute_score(llm_ans_dict[k], ans_dict[k])[0]
                scores[k] = {
                    'ROUGE-L': rouge,
                    'CIDEr': cider,
                }
            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'scores': scores,
                'avg_score': {
                    'ROUGE-L': Rouge().compute_score(overall_llm_ans, overall_ans)[0],
                    'CIDEr': Cider().compute_score(overall_llm_ans, overall_ans)[0],
                }
            }
        json.dump(res, open(no_ctx_save_path, 'w'), indent=4)

        ### w/ context
        res = self._init_result()
        for f in self.ctx_files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f, 'ctx')
            llm_ans_dict = {}
            ans_dict = {}
            overall_llm_ans = {}
            overall_ans = {}
            cnt = {}
            for i, ds in enumerate(llm_res):
                for j, d in enumerate(ds['questions']):
                    if ds['type'][j] == 1 and self.ctx_data[i].get('unique_ans', [0 for _ in range(j + 1)])[j] == 1:
                        cate = self.ctx_data[i]['category'][j]
                        cate_cnt = cnt.get(cate, 0)
                        cnt[cate] = cate_cnt + 1

                        ans = ds['answers'][j]
                        llm_ans = ds['llm_answer'][j]

                        if llm_ans == "" or llm_ans is None:
                            llm_ans = "No answer provided."

                        tmp1 = llm_ans_dict.get(cate, {})
                        tmp1[f'{i}_{j}'] = [llm_ans]
                        llm_ans_dict[cate] = tmp1

                        tmp2 = ans_dict.get(cate, {})
                        tmp2[f'{i}_{j}'] = [ans]
                        ans_dict[cate] = tmp2

                        overall_llm_ans[f'{i}_{j}'] = [llm_ans]
                        overall_ans[f'{i}_{j}'] = [ans]

            scores = {}
            for k in cnt.keys():
                rouge = Rouge().compute_score(llm_ans_dict[k], ans_dict[k])[0]
                cider = Cider().compute_score(llm_ans_dict[k], ans_dict[k])[0]
                scores[k] = {
                    'ROUGE-L': rouge,
                    'CIDEr': cider,
                }

            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'scores': scores,
                'avg_score': {
                    'ROUGE-L': Rouge().compute_score(overall_llm_ans, overall_ans)[0],
                    'CIDEr': Cider().compute_score(overall_llm_ans, overall_ans)[0],
                }
            }
        json.dump(res, open(ctx_save_path, 'w'), indent=4)

    # We use GPT-4 to evaluate short answer questions
    def evaluate_sa(self):

        res = self._init_result()
        no_ctx_save_path, ctx_save_path = self._path_format('sa')
        api = ApiManager(
            model_name='gpt-4',
            seed=41,
            default_max_tokens=20,
            temperature=0,
        )
        prompt_SA_EVAL = '''You are a NLP professional assistant, your work is to evaluate whether the student's answer is correct for the given short answer question. 
        A teacher answer is also provided, your evaluation should based on the teacher answer.
        If the student is correct, return 1, else return 0.
        Your response should ONLY contain 0 or 1.

        Short answer question:
        "{q}"
        
        Teacher answer:
        "{eg_ans}"

        Student answer (evaluate this answer):
        "{llm_ans}"

        Your response:
        '''

        for f in self.no_ctx_files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f)
            corr = {c: 0 for c in cates}
            cnt = {c: 0 for c in cates}
            for i, d in enumerate(llm_res):
                if d['type'] == 1:
                    print(f'Processing Q.{i}')
                    cate = self.no_ctx_data[i]['category']
                    cate_cnt = cnt.get(cate, 0)
                    cnt[cate] = cate_cnt + 1

                    q = d['question']
                    ans = d['answer']
                    llm_ans = d['llm_answer']
                    if llm_ans == "" or llm_ans is None:
                        llm_ans = "No answer provided."

                    score = api(
                        [{'role': 'user', 'content': prompt_SA_EVAL.format(q=q, eg_ans=ans, llm_ans=llm_ans)}]
                    )
                    try:
                        score = int(score)
                    except ValueError:
                        score = 0
                    if score == 1:
                        cate_ans = corr.get(cate, 0)
                        corr[cate] = cate_ans + 1
                    else:
                        cate_ans = corr.get(cate, 0)
                        corr[cate] = cate_ans
                    d['retrived_answer'] = score

            acc = {k: v / cnt[k] if cnt[k] != 0 else 1 for k, v in corr.items()}
            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            overall_acc = np.sum(np.array(list(acc.values())) * np.array(list(cnt.values()))) / sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'acc': acc,
                'overall_acc': overall_acc
            }
            json.dump(llm_res, open(f'res/{self.seed}{self.osd}/no_ctx/{f}', 'w'), indent=4)
        json.dump(res, open(no_ctx_save_path, 'w'), indent=4)

        ### w/ context
        res = self._init_result()
        for f in self.ctx_files:
            llm_name, shot_type, prompt_r, llm_res = self._file_format(f, 'ctx')
            corr = {c: 0 for c in cates}
            cnt = {c: 0 for c in cates}
            for i, ds in enumerate(llm_res):
                tmp = []
                for j, d in enumerate(ds['questions']):
                    if ds['type'][j] == 1:
                        print(f'Processing Q.{i}_{j}')
                        cate = self.ctx_data[i]['category'][j]
                        cate_cnt = cnt.get(cate, 0)
                        cnt[cate] = cate_cnt + 1

                        q = ds['questions'][j]
                        ans = ds['answers'][j]
                        llm_ans = ds['llm_answer'][j]
                        if llm_ans == "" or llm_ans is None:
                            llm_ans = "No answer provided."

                        score = api(
                            [{'role': 'user', 'content': prompt_SA_EVAL.format(q=q, eg_ans=ans, llm_ans=llm_ans)}]
                        )
                        try:
                            score = int(score)
                        except ValueError:
                            print('err: ', score)
                            score = 0
                        if score == 1:
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans + 1
                        else:
                            cate_ans = corr.get(cate, 0)
                            corr[cate] = cate_ans
                        tmp.append(score)
                ds['retrived_answer'] = tmp

            acc = {k: v / cnt[k] if cnt[k] != 0 else 1 for k, v in corr.items()}
            res['count'] = cnt
            res['total_count'] = sum(cnt.values())
            overall_acc = np.sum(np.array(list(acc.values())) * np.array(list(cnt.values()))) / sum(cnt.values())
            res[llm_name][f'{shot_type}{prompt_r}'] = {
                'acc': acc,
                'overall_acc': overall_acc
            }
            json.dump(llm_res, open(f'res/{self.seed}{self.osd}/ctx/{f}', 'w'), indent=4)
        json.dump(res, open(ctx_save_path, 'w'), indent=4)


if __name__ == '__main__':
    eval_mg = Evaluation(41, False)
    eval_mg_oc = Evaluation(41, True)

    eval_mg.evaluate_mc()
    eval_mg.evaluate_sa()
    eval_mg.evaluate_sc()
    eval_mg.evaluate_sa_unique()

    eval_mg_oc.evaluate_mc()
    eval_mg_oc.evaluate_sa()
    eval_mg_oc.evaluate_sc()
    eval_mg_oc.evaluate_sa_unique()
