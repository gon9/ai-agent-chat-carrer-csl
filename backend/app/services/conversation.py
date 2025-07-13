from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
from datetime import datetime
from app.schemas.chat import ChatMessage, Conversation
from app.services.agent import process_message

# 会話を保存するためのインメモリストレージ
# 実際のアプリケーションではデータベースを使用することを推奨
conversations: Dict[UUID, Conversation] = {}


async def get_conversation(conversation_id: UUID) -> Optional[Conversation]:
    """
    指定されたIDの会話を取得する
    """
    return conversations.get(conversation_id)


async def create_conversation() -> Conversation:
    """
    新しい会話を作成する
    """
    conversation = Conversation()
    conversations[conversation.id] = conversation
    return conversation


async def add_message_to_conversation(
    conversation_id: UUID, role: str, content: str
) -> ChatMessage:
    """
    会話にメッセージを追加する
    """
    conversation = await get_conversation(conversation_id)
    if not conversation:
        conversation = await create_conversation()
        conversation.id = conversation_id
    
    message = ChatMessage(role=role, content=content)
    conversation.messages.append(message)
    conversation.updated_at = datetime.now()
    
    return message


async def handle_chat_request(
    message: str, conversation_id: Optional[UUID] = None, metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    チャットリクエストを処理し、AIの応答を返す
    """
    # 会話IDがない場合は新しい会話を作成
    if not conversation_id:
        conversation = await create_conversation()
        conversation_id = conversation.id
    else:
        conversation = await get_conversation(conversation_id)
        if not conversation:
            conversation = await create_conversation()
            conversation.id = conversation_id
    
    # ユーザーメッセージを会話に追加
    await add_message_to_conversation(conversation_id, "user", message)
    
    # コンテキストの準備
    context = metadata or {}
    
    # 過去の会話履歴をコンテキストに追加
    if conversation and conversation.messages:
        # 最新の5つのメッセージのみを使用（パフォーマンスのため）
        recent_messages = conversation.messages[-5:]
        context["history"] = [
            {"role": msg.role, "content": msg.content} for msg in recent_messages
        ]
    
    # エージェントにメッセージを処理させる
    response = await process_message(message, conversation_id, context)
    
    # AIの応答を会話に追加
    if not response.get("error"):
        await add_message_to_conversation(conversation_id, "assistant", response["message"])
    
    return response
