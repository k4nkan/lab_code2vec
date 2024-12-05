import ast
import numpy as np

def code_to_ast(code):
    try:
        tree = ast.parse(code)
    # エラーハンドリング
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        return np.array([])

    vector = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            vector.append(0)
        elif isinstance(node, ast.Expr):
            vector.append(1)
        elif isinstance(node, ast.Call):
            vector.append(2)
        elif isinstance(node, ast.FunctionDef):
            vector.append(3)
    return np.array(vector)

def main():
    # コードを読み取り
    try:
        with open("../test_data/code_1.txt", "r") as file:
            code = file.read()
    except FileNotFoundError:
        print("code_1.txt が見つかりません。")
        return

    # ASTに変換
    vector = code_to_ast(code)

    print("読み取ったコード:")
    print(code)
    print("\nASTベクトル:")
    print(vector)

if __name__ == "__main__":
    main()
