import ast

# ASTパスを収集する関数
def extract_ast_paths(node, parent_path=None):
    # 親ノードの初期化、再帰の際の更新
    if parent_path is None:
        parent_path = []

    # 現在のノードの情報を取得
    current_node = type(node).__name__
    current_path = parent_path + [current_node]

    # これまでのノードまでのパスを作成
    paths = [current_path]

    # 再帰
    for child in ast.iter_child_nodes(node):
        paths.extend(extract_ast_paths(child, current_path))

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
        with open("../test_data/code_1.txt", "r") as file:
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
