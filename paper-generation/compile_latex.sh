#!/bin/bash

# コンパイルする LaTeX ファイルの名前（拡張子なし）
FILENAME="main_draft"

# 補助ファイルを出力する一時ディレクトリ
TEMP_DIR="./auxiliary_files"

# 一時ディレクトリがなければ作成
mkdir -p $TEMP_DIR

# pdflatex を使用してファイルをコンパイル
pdflatex -output-directory=$TEMP_DIR $FILENAME.tex

# PDF ファイルをカレントディレクトリに移動
mv $TEMP_DIR/$FILENAME.pdf ./
