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
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        return []

    return extract_ast_paths(tree)

# ウィンドウサイズ3でパスコンテキストを生成
def generate_context_windows(paths, window_size=3):
    context_windows = []
    half_window = window_size // 2

    for path in paths:
        path_length = len(path)
        for i in range(path_length):
            # ウィンドウの範囲を定義
            start_idx = max(0, i - half_window)
            end_idx = min(path_length, i + half_window + 1)

            # ウィンドウをスライスして追加
            context_window = path[start_idx:end_idx]
            context_windows.append(context_window)

    return context_windows

def main():
    try:
        with open("../../test_data/code_1.txt", "r") as file:
            code = file.read()
    except FileNotFoundError:
        print("code_1.txt が見つかりません。")
        return

    # ASTパスに変換
    paths = code_to_ast_paths(code)

    print("ASTのパス:")
    for path in paths:
        print(" -> ".join(path))

    # ウィンドウサイズ3のコンテキスト生成
    window_size = 3
    context_windows = generate_context_windows(paths, window_size)

    print("\nウィンドウサイズ3のコンテキスト:")
    for window in context_windows:
        print(" | ".join(window))

if __name__ == "__main__":
    main()
