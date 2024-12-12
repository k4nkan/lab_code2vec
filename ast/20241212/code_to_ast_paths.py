import ast
from collections import deque

# ASTパスを収集
def extract_ast_paths(node, parent_path=None):
    if parent_path is None:
        parent_path = deque()

    # 現在のノードを追加
    parent_path.append(type(node).__name__)

    # パスをリストに追加
    paths = [list(parent_path)]

    # 子ノードを探索
    for child in ast.iter_child_nodes(node):
        paths.extend(extract_ast_paths(child, parent_path))

    # 現在のノードを削除
    parent_path.pop()

    return paths

# コードをASTパスベクトルに変換
def code_to_ast_paths(code):
    # コードをastに変換
    try:
        tree = ast.parse(code)
    # エラーハンドリング
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        return []

    return extract_ast_paths(tree)

def main():
    # テストデータのロード
    try:
        with open("../../test_data/code_1.txt", "r") as file:
            code = file.read()
    # エラーハンドリング
    except FileNotFoundError:
        print("code_1.txt が見つかりません。")
        return

    # ASTパスに変換
    paths = code_to_ast_paths(code)

    # 結果を表示
    print("ASTのパス:")
    for path in paths:
        print(" -> ".join(path))

if __name__ == "__main__":
    main()
