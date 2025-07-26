#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
from langgraph.graph import END

# agent.pyからグラフ構造を取得するための最小限のコード
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# シンプルなグラフを作成
G = nx.DiGraph()

# agent.pyの構造を反映したノードとエッジを追加
G.add_nodes_from([("career_counselor", {"label": "キャリアカウンセラー"}), 
                  ("it_specialist", {"label": "ITスキル専門家"}), 
                  ("response_generation", {"label": "レスポンス生成"}), 
                  ("END", {"label": "終了"})])

G.add_edges_from([("career_counselor", "it_specialist", {"label": "it_consultation=True"}), 
                  ("career_counselor", "response_generation", {"label": "it_consultation=False"}),
                  ("it_specialist", "response_generation", {"label": "常に"}),
                  ("response_generation", "END", {"label": "常に"})])

# グラフを描画して保存
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, "label"), 
       node_color=["lightblue", "lightgreen", "lightyellow", "lightgray"], node_size=2000)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "label"))
plt.axis("off")
plt.savefig("agent_graph.png", dpi=300, bbox_inches="tight")
print("グラフ画像が agent_graph.png として保存されました。")

# macOSで画像を開く
if sys.platform == "darwin":
    os.system("open agent_graph.png")

