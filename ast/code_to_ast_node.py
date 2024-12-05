import ast

# ASTパスを収集する関数
def extract_ast_paths(node, parent_path=None):
    if parent_path is None:
        parent_path = []

    current_node = type(node).__name__
    current_path = parent_path + [current_node]
    paths = [current_path]

    for child in ast.iter_child_nodes(node):
        paths.extend(extract_ast_paths(child, current_path))

    return paths

# コードをASTパスベクトルに変換
def code_to_ast_paths(code):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        return []

    return extract_ast_paths(tree)

def main():
    try:
        with open("../test_data/code_1.txt", "r") as file:
            code = file.read()
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
