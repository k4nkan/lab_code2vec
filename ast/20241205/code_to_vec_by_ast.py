import ast
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from textwrap import dedent

# 1. コードをASTパスに変換する関数
def extract_ast_paths(code):
    """
    Pythonコードを抽象構文木（AST）として解析し、ASTパスを抽出。
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"構文エラーが発生しました: {e}")
        return []

    def visit(node, path=None):
        if path is None:
            path = []
        if not isinstance(node, ast.AST):
            return []
        paths = [path + [type(node).__name__]]
        for child in ast.iter_child_nodes(node):
            paths += visit(child, path + [type(node).__name__])
        return paths

    paths = visit(tree)
    if not paths:
        print(f"ASTパスが抽出できませんでした: {code}")
    return ["->".join(p) for p in paths]

# 2. 入力コードリスト（インデントを自動調整）
codes = [
    dedent("""
    def add(a, b):
        return a + b
    """),
    dedent("""
    def subtract(a, b):
        return a - b
    """),
    dedent("""
    def multiply(a, b):
        return a * b
    """),
    dedent("""
    def greet(name):
        print(f"Hello, {name}!")
    """),
    dedent("""
    def add_numbers(x, y):
        return x + y
    """)
]

# 3. ASTパスを抽出
ast_paths = [extract_ast_paths(code) for code in codes]

# 4. パスを文字列に変換（空のエントリを除外）
path_texts = [" ".join(paths) for paths in ast_paths if paths]
if not path_texts:
    raise ValueError("ASTパスが抽出されませんでした。入力コードを確認してください。")

print("path_textsの内容:")
for i, text in enumerate(path_texts):
    print(f"Code {i+1}: {text}")

# 5. ベクトル化 (CountVectorizerを使用)
vectorizer = CountVectorizer()
code_vectors = vectorizer.fit_transform(path_texts).toarray()

# 6. 類似度計算
similarity_matrix = cosine_similarity(code_vectors)

print("類似度マトリクス:")
print(similarity_matrix)

# 7. クラスタリング (K-means)
n_clusters = 2  # クラスタ数
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
labels = kmeans.fit_predict(code_vectors)

print("\nクラスタリング結果（各コードのクラスタID）:")
for i, label in enumerate(labels):
    print(f"コード {i+1}: クラスタ {label}")

# 8. 次元削減と可視化 (t-SNE)
tsne = TSNE(n_components=2, random_state=0)
reduced_vectors = tsne.fit_transform(code_vectors)

plt.figure(figsize=(8, 6))
plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], c=labels, cmap='viridis', s=100)
for i, code in enumerate(codes):
    plt.text(reduced_vectors[i, 0], reduced_vectors[i, 1], f"Code {i+1}", fontsize=12)
plt.title("コード類似度の可視化")
plt.colorbar(label='クラスタ')
plt.show()
