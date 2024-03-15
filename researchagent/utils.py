import re

def _parse_latex(path):
    # LaTeXファイルを読み込む
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

    # abstractの抽出
    abstract_match = re.search(r'\\begin{abstract}(.+?)\\end{abstract}', text, re.DOTALL)
    abstract_text = abstract_match.group(1).strip() if abstract_match else ""

    # セクションを抽出するための正規表現パターン
    section_pattern = r'\\section\{(.+?)\}'
    sections = re.findall(section_pattern, text)

    # パースしたデータを保存するリスト
    parsed_data = []

    # 最初にabstractを追加
    parsed_data.append({
        "sentences": re.split(r'(?<=[.!?]) +', abstract_text),
        "section": {
            "title": "Abstract",
            "number": 0
        }
    })

    # 各セクションのテキストを抽出し、それを分析する
    for i, section in enumerate(sections, start=1):  # start=1 でセクション番号を開始
        start = re.search(r'\\section\{' + re.escape(section) + r'\}', text).end()
        # 次のセクションまたは\bibliographyが見つかった場合
        next_section_match = re.search(r'\\section\{', text[start:])
        bibliography_match = re.search(r'\\bibliography\{', text[start:])

        # 次のセクションまたは\bibliographyが見つかった場合
        if next_section_match or bibliography_match:
            # 次のセクションと\bibliographyのどちらが先に出現するかを判断
            end = min(
                next_section_match.start() if next_section_match else len(text),
                bibliography_match.start() if bibliography_match else len(text)
            ) + start
        else:
            # どちらも存在しない場合はファイルの終わりまでをセクションの終わりとする
            end = len(text)

        # セクションテキストを抽出
        section_text = text[start:end].strip()

        # パラグラフに分割
        paragraphs = section_text.split('\n\n')

        # 各パラグラフを文に分割して結果に追加
        for paragraph in paragraphs:
            parsed_data.append({
                "sentences": re.split(r'(?<=[.!?]) +', paragraph.strip()),  # TODO: 文に分割しないでパラグラフのまま返すのでもいいかも
                "section": {
                    "title": section,
                    "number": i
                }
            })

    return parsed_data