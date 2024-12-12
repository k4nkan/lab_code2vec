import ast
from collections import deque

# ASTパスを収集
def extract_ast_paths(node, parent_path=None):
    if parent_path is None:
        parent_path = deque()  # 現在のノードまでのパスを保持するデック

    parent_path.append(type(node).__name__)  # 現在のノードの型名をパスに追加
    paths = [list(parent_path)]  # 現在のパスを保存

    # 子ノードを再帰的に探索してパスを収集
    for child in ast.iter_child_nodes(node):
        paths.extend(extract_ast_paths(child, parent_path))

    parent_path.pop()  # 現在のノードを探索終了後にパスから削除
    return paths

# コードをASTパスベクトルに変換
def code_to_ast_paths(code):
    try:
        tree = ast.parse(code)  # コードを解析してASTツリーを生成
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        return []
    return extract_ast_paths(tree)

# ウィンドウサイズ3でパスコンテキストを生成
def generate_context_windows(paths, window_size=3):
    context_windows = []
    half_window = window_size // 2  # ウィンドウの中央位置を計算

    # 各パスからコンテキストウィンドウを生成
    for path in paths:
        path_length = len(path)
        for i in range(path_length):
            # 現在のノードを中心にウィンドウの範囲を計算
            start_idx = max(0, i - half_window)
            end_idx = min(path_length, i + half_window + 1)
            context_window = path[start_idx:end_idx]  # 部分的なパスをスライス
            context_windows.append(context_window)  # コンテキストウィンドウを保存

    return context_windows

# 辞書の作成
def build_node_dictionary(paths):
    # 全パスに含まれるユニークなノードを収集
    unique_nodes = set(node for path in paths for node in path)
    # ノードに一意のインデックスを割り振る辞書を作成
    node_dict = {node: idx for idx, node in enumerate(sorted(unique_nodes))}
    return node_dict

# ベクトル化
def vectorize_context_windows(context_windows, node_dict):
    vectorized_windows = []
    # 各ウィンドウ内のノードを辞書のインデックスで置き換え
    for window in context_windows:
        vectorized_window = [node_dict[node] for node in window]
        vectorized_windows.append(vectorized_window)  # ベクトル化したウィンドウを保存
    return vectorized_windows


# メイン関数
def main():
    # ファイルの読み込み
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

    # ノード辞書の作成
    node_dict = build_node_dictionary(paths)
    print("\nノード辞書:", node_dict)

    # ベクトル化
    vectorized_windows = vectorize_context_windows(context_windows, node_dict)
    print("\nベクトル化されたウィンドウ:")
    for vector in vectorized_windows:
        print(vector)

if __name__ == "__main__":
    main()
