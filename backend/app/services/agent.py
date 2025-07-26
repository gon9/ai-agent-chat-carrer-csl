from typing import Dict, List, Any, Annotated, Sequence, Literal, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field
import json
import random
from uuid import UUID
from app.core.config import settings
from app.services.prompts import CAREER_COUNSELOR_PROMPT, IT_SPECIALIST_PROMPT, RESPONSE_GENERATION_PROMPT


class AgentState(BaseModel):
    """エージェントの状態を表す型"""
    messages: Sequence[BaseMessage] = Field(description="これまでの会話履歴")
    context: Dict[str, Any] = Field(default_factory=dict, description="コンテキスト情報")
    it_consultation: bool = Field(default=False, description="ITスキル専門家への相談が必要かどうか")
    it_advice: str = Field(default="", description="ITスキル専門家からのアドバイス")
    next: Literal["career_counselor", "it_specialist", "response_generation"] = Field(
        default="career_counselor", description="次のノード"
    )


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

    # プロンプトはprompts.pyからインポート

    # キャリアカウンセラーノードの定義
    def career_counselor_node(state: AgentState) -> AgentState:
        """キャリアカウンセラーの処理を行うノード"""
        messages = state.messages
        
        # 最後のユーザーメッセージを取得
        last_user_message = next((msg.content for msg in reversed(messages) if isinstance(msg, HumanMessage)), "")
        
        # コンテキストからロール情報を取得（デフォルトはキャリアカウンセラー）
        role = state.context.get("selected_role", "career_counselor")
        
        # ロールに応じたプロンプトを選択
        if role == "it_specialist":
            system_prompt = f"""
            あなたはITスキル専門家です。ユーザーのIT関連のキャリア相談に対して、
            技術トレンド、必要なスキル、学習リソース、キャリアパスについて
            具体的で実用的なアドバイスを提供してください。
            
            ユーザーの質問: {last_user_message}
            """
        else:  # デフォルトはキャリアカウンセラー
            system_prompt = f"""
            あなたはキャリアカウンセラーです。ユーザーのキャリア相談に対して、
            親身に、かつ専門的な知識をもとにアドバイスを提供してください。
            キャリア選択、転職、スキルアップ、職場の人間関係など、
            幅広いキャリアに関する質問に対応してください。
            
            ユーザーの質問: {last_user_message}
            """
        
        # プロンプトの作成
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", last_user_message)
        ])
        
        # LLMに質問を投げる
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({})
        
        # AIメッセージを作成
        ai_message = AIMessage(content=response)
        
        # 新しい状態を作成
        new_state = state.model_copy()
        new_state.messages = list(state.messages) + [ai_message]
        new_state.next = None  # 処理終了
        return new_state
    
    # # ITスキル専門家ノードの定義
    # def it_specialist_node(state: AgentState) -> AgentState:
    #     """ITスキル専門家の処理を行うノード"""
    #     messages = state.messages
        
    #     # 最後のユーザーメッセージを取得
    #     last_user_message = next((msg.co`ntent for msg in reversed(messages) if isinstance(msg, HumanMessage)), "")
        
    #     # ITスキル専門家のプロンプト作成
    #     prompt = ChatPromptTemplate.from_messages([
    #         ("system", IT_SPECIALIST_PROMPT),
    #         ("human", "{input}")
    #     ])
        
    #     # LLMに質問を投げる
    #     chain = prompt | llm | StrOutputParser()
    #     it_advice = chain.invoke({"input": last_user_message})
        
    #     # 新しい状態を作成
    #     new_state = state.model_copy()
    #     new_state.it_advice = it_advice
    #     new_state.next = "response_generation"
    #     return new_state
    
    # レスポンス生成ノードの定義
    def response_generation_node(state: AgentState) -> AgentState:
        """最終的な応答を生成するノード"""
        messages = state.messages
        it_advice = state.it_advice
        it_consultation = state.it_consultation
        
        # 最後のユーザーメッセージを取得
        last_user_message = next((msg.content for msg in reversed(messages) if isinstance(msg, HumanMessage)), "")
        
        # レスポンス生成プロンプト作成
        # システムプロンプトを直接作成
        system_prompt = f"""
        あなたはキャリアカウンセラーのAIアシスタントです。
        ユーザーのキャリア相談に対して、親身に、かつ専門的な知識をもとにアドバイスを提供してください。
        
        ユーザーの質問: {last_user_message}
        
        IT専門家への相談が必要かどうか: {it_consultation}
        
        以下のITスキル専門家からのアドバイスも参考にして、総合的な回答を作成してください。
        ITスキル専門家のアドバイス: {it_advice}
        
        ユーザーの状況を理解し、具体的で実用的なアドバイスを心がけてください。
        ITスキル専門家からのアドバイスを自然に取り入れ、一責性のある回答を作成してください。
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", last_user_message)
        ])
        
        # LLMに質問を投げる
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({})
        
        # AIMessageを作成
        ai_message = AIMessage(content=response)
        
        # 新しい状態を作成
        new_state = state.model_copy()
        new_state.messages = messages + [ai_message]
        new_state.next = END
        return new_state
    
    # ルーターの定義
    def router(state: AgentState) -> Literal["career_counselor", "it_specialist", "response_generation"]:
        return state.next

    # グラフの構築
    workflow = StateGraph(AgentState)
    
    # ノードの追加 - キャリアカウンセラーノードのみ使用
    workflow.add_node("career_counselor", career_counselor_node)
    
    # エントリーポイントの設定
    workflow.set_entry_point("career_counselor")
    
    # キャリアカウンセラーノードから直接終了する
    # ENDはグラフの終了を表す定数
    workflow.add_edge("career_counselor", END)
    
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
    def mock_agent_node(state: AgentState) -> AgentState:
        """モックエージェントの処理を行うノード"""
        messages = state.messages
        context = state.context
        
        # ランダムな応答を選択
        response_text = random.choice(mock_responses)
        response = AIMessage(content=response_text)
        
        # 新しい状態を返す
        new_state = state.model_copy()
        new_state.messages = list(messages) + [response]
        return new_state

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
    """ユーザーメッセージを処理し、AIの応答を返す"""
    try:
        # 入力値のバリデーション
        if not message or message == "string":
            # メッセージが空またはデフォルト値の場合はエラー
            return {
                "message": "有効なメッセージを入力してください。",
                "conversation_id": conversation_id,
                "metadata": context,
                "error": "無効なメッセージ内容"
            }
            
        # メッセージをHumanMessageに変換
        human_message = HumanMessage(content=message)
        
        # コンテキストがなければ空の辞書を使用
        if context is None:
            context = {}
        
        # 会話履歴が空の場合は初期化
        messages = [human_message]
        
        print(f"\n[DEBUG] メッセージ処理開始: {message}")
        print(f"[DEBUG] コンテキスト: {context}")
        
        # エージェントグラフを実行
        agent_state = AgentState(
            messages=messages, 
            context=context,
            it_consultation=False,
            it_advice="",
            next="career_counselor"
        )
        
        result = await agent_graph.ainvoke(agent_state)
        
        print(f"[DEBUG] エージェントグラフ実行完了")
        print(f"[DEBUG] 結果の型: {type(result)}")
        print(f"[DEBUG] 結果の内容: {result}")
        
        # AIの応答を取得
        # resultがNoneの場合のエラーハンドリング
        if result is None:
            print(f"[ERROR] エージェント結果がNoneです")
            return {
                "message": "申し訳ありません。応答を生成できませんでした。",
                "conversation_id": conversation_id,
                "metadata": context
            }
        elif isinstance(result, dict):
            # 返値が辞書型の場合
            if "messages" in result:
                # messagesキーがあればそこから取得
                messages = result["messages"]
                if messages is None:
                    print(f"[ERROR] messagesがNoneです")
                    return {
                        "message": "申し訳ありません。応答を生成できませんでした。",
                        "conversation_id": conversation_id,
                        "metadata": context
                    }
                ai_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
            else:
                # 直接メッセージを生成
                return {
                    "message": str(result.get("output", "応答を生成できませんでした")),
                    "conversation_id": conversation_id,
                    "metadata": context
                }
        else:
            # AgentState型の場合
            # result.messagesがNoneの場合のエラーハンドリング
            if not hasattr(result, 'messages') or result.messages is None:
                print(f"[ERROR] result.messagesが存在しないか、Noneです")
                return {
                    "message": "申し訳ありません。応答を生成できませんでした。",
                    "conversation_id": conversation_id,
                    "metadata": context
                }
            ai_messages = [msg for msg in result.messages if isinstance(msg, AIMessage)]
        
        if ai_messages:
            response_content = ai_messages[-1].content
            return {
                "message": response_content,
                "conversation_id": conversation_id,
                "metadata": context
            }
        else:
            return {
                "message": "申し訳ありません。応答を生成できませんでした。",
                "conversation_id": conversation_id,
                "metadata": context
            }
    except Exception as e:
        print(f"[ERROR] メッセージ処理中にエラーが発生しました: {str(e)}")
        import traceback
        print(f"[ERROR] スタックトレース: {traceback.format_exc()}")
        return {
            "message": f"申し訳ありません。メッセージ処理中にエラーが発生しました: {str(e)}",
            "conversation_id": conversation_id,
            "metadata": context,
            "error": str(e)
        }
