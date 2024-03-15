'''
文章などはすでに生成されていると仮定して、この python ファイルではあくまでそれらを貼り合わせて neurips の論文にフォーマッティングするところにだけ集中する
'''

import subprocess

# TODO: ひとまず保存されてる情報をそのまま出力するものを作るが、将来的にはLLMの出力を使うように変更する

def update_main_tex(**kwargs):
    main_tex_path = kwargs['main_tex_path']
    abstract_path = kwargs['abstract_path']
    introduction_path = kwargs['introduction_path']
    method_path = kwargs['method_path']
    summary_txt_path = kwargs['summary_txt_path']
    dataset_description_path = kwargs['dataset_description_path']
    model_description_path = kwargs['model_description_path']
    experiment_results_path = kwargs['experiment_results_path']
    conclusion_path = kwargs['conclusion_path']

    # 論文の更新する中身を読み込む
    with open(abstract_path, 'r', encoding='utf-8') as file:
        abstract = file.read()
    with open(introduction_path, 'r', encoding='utf-8') as file:
        introduction = file.read()
    with open(method_path, 'r', encoding='utf-8') as file:
        method = file.read()
    with open(summary_txt_path, 'r', encoding='utf-8') as file:
        experiment_summary = file.read()
    with open(dataset_description_path, 'r', encoding='utf-8') as file:
        dataset_description = file.read()
    with open(model_description_path, 'r', encoding='utf-8') as file:
        model_description = file.read()
    with open(experiment_results_path, 'r', encoding='utf-8') as file:
        experiment_results = file.read()  
    with open(conclusion_path, 'r', encoding='utf-8') as file:
        conclusion = file.read()  

    # main.tex を読み込む
    with open('main.tex', 'r', encoding='utf-8') as file:
        tex_content = file.read()

    # プレースホルダーを実験設計の要約で置き換え
    tex_content = tex_content.replace("{abstract-description}", abstract)
    tex_content = tex_content.replace("{introduction-description}", introduction)
    tex_content = tex_content.replace("{method-description}", method)
    tex_content = tex_content.replace("{experiment-design-summary}", experiment_summary)
    tex_content = tex_content.replace("{dataset-description}", dataset_description)
    tex_content = tex_content.replace("{model-description}", model_description)
    tex_content = tex_content.replace("{experiment-results}", experiment_results)
    tex_content = tex_content.replace("{conclusion-description}", conclusion)

    # 更新された内容で main.tex を上書きし main_draft.tex として保存
    with open(main_tex_path, 'w', encoding='utf-8') as file:
        file.write(tex_content)

# スクリプトを実行
paths = {
    'main_tex_path': 'main_draft.tex',
    'abstract_path': '../outputs/abstract.txt',
    'introduction_path': '../outputs/introduction.txt',
    'method_path': '../outputs/method.txt',
    'summary_txt_path': '../outputs/experiment_design_summary.txt',
    'dataset_description_path': '../outputs/dataset_description.txt',
    'model_description_path': '../outputs/model_description.txt',
    'experiment_results_path': '../outputs/experiment_results.txt',
    'conclusion_path': '../outputs/conclusion.txt'
}
update_main_tex(**paths)


subprocess.run(["./compile_latex.sh"])