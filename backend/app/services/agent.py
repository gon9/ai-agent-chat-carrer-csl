from typing import Dict, List, Any, TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os
import random
from uuid import UUID
from app.core.config import settings


class AgentState(TypedDict):
    """エージェントの状態を表す型"""
    messages: Annotated[Sequence[BaseMessage], "これまでの会話履歴"]
    context: Dict[str, Any]


def create_agent_graph():
    """
    LangGraphを使用したエージェントグラフを作成する
    """
    # OpenAIのAPIキーが設定されていることを確認
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
        print("Warning: OPENAI_API_KEY is not set or is using default value. Using mock responses.")
        return create_mock_agent_graph()
    
    try:
        # LLMの初期化
        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_NAME,
            temperature=0.7,
        )
    except Exception as e:
        print(f"Error initializing ChatOpenAI: {e}")
        return create_mock_agent_graph()

    # システムプロンプトの設定
    system_prompt = """
    あなたはキャリアカウンセラーのAIアシスタントです。
    ユーザーのキャリア相談に対して、親身に、かつ専門的な知識をもとにアドバイスを提供してください。
    ユーザーの状況を理解し、具体的で実用的なアドバイスを心がけてください。
    """

    # エージェントノードの定義
    def agent_node(state: AgentState) -> dict:
        """エージェントの主要な処理を行うノード"""
        messages = state["messages"]
        context = state.get("context", {})
        
        # システムプロンプトを先頭に追加（まだない場合）
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            messages = [SystemMessage(content=system_prompt)] + list(messages)
        
        # LLMに質問を投げる
        response = llm.invoke(messages)
        
        # 新しい状態を返す
        return {"messages": messages + [response], "context": context}

    # グラフの構築
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    
    # エッジの定義
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    # グラフのコンパイル
    return workflow.compile()


def create_mock_agent_graph():
    """
    OpenAI APIキーが設定されていない場合に使用するモックエージェントグラフを作成する
    """
    # モック応答のリスト
    mock_responses = [
        "キャリア選択において重要なのは、自分の強みと情熱を理解することです。あなたの強みはどのような分野にありますか？",
        "転職を考える際は、現在のスキルセットと市場のニーズのギャップを分析することが大切です。具体的にどのようなスキルを身につけたいですか？",
        "キャリアパスを考える上で、短期目標と長期目標を明確にすることが重要です。5年後にはどのようなポジションを目指していますか？",
        "職場環境も重要な要素です。どのような企業文化や働き方があなたに合っていると思いますか？",
        "スキルアップのためには継続的な学習が欠かせません。最近取り組んでいる学習や興味のある分野はありますか？",
        "ワークライフバランスも大切な要素です。理想的な働き方について教えてください。",
        "キャリア開発には人脈も重要です。業界内でのネットワーキングはどのように行っていますか？",
        "自己分析は継続的に行うことが大切です。最近気づいた自分の強みや弱みはありますか？"
    ]
    
    # エージェントノードの定義
    def mock_agent_node(state: AgentState) -> dict:
        """モックエージェントの処理を行うノード"""
        messages = state["messages"]
        context = state.get("context", {})
        
        # ランダムな応答を選択
        response_text = random.choice(mock_responses)
        response = AIMessage(content=response_text)
        
        # 新しい状態を返す
        return {"messages": messages + [response], "context": context}

    # グラフの構築
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", mock_agent_node)
    
    # エッジの定義
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    # グラフのコンパイル
    return workflow.compile()


# グラフのインスタンスを作成
agent_graph = create_agent_graph()


async def process_message(message: str, conversation_id: UUID = None, 
                         context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    ユーザーメッセージを処理し、AIの応答を返す
    """
    # 初期状態の設定
    state = {
        "messages": [HumanMessage(content=message)],
        "context": context or {}
    }
    
    # エージェントグラフの実行
    result = agent_graph.invoke(state)
    
    # 結果から最後のAIメッセージを取得
    ai_message = next((msg for msg in reversed(result["messages"]) 
                      if isinstance(msg, AIMessage)), None)
    
    if not ai_message:
        return {"message": "応答の生成に失敗しました", "error": True}
    
    return {
        "message": ai_message.content,
        "conversation_id": conversation_id,
        "metadata": result.get("context", {})
    }
