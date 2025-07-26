from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage
from app.services.conversation import handle_chat_request, get_conversation, create_conversation, get_all_conversation_ids

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    チャットメッセージを処理し、AIの応答と会話履歴を返す
    会話IDが提供されていない場合は新しい会話を自動的に作成する
    """
    try:
        # メッセージ処理
        response = await handle_chat_request(
            message=request.message,
            conversation_id=request.conversation_id,
            metadata=request.metadata
        )
        
        # 会話の取得（最新の状態）
        conversation = await get_conversation(response["conversation_id"])
        
        return ChatResponse(
            message=response["message"],
            conversation_id=response["conversation_id"],
            messages=conversation.messages,
            metadata=response.get("metadata")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"チャット処理中にエラーが発生しました: {str(e)}")


# 不要なエンドポイント（get_conversation_by_id）を削除


@router.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessage])
async def get_conversation_messages(conversation_id: UUID) -> List[ChatMessage]:
    """
    指定された会話のメッセージを取得する
    """
    conversation = await get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail=f"ID {conversation_id} の会話が見つかりません")
    return conversation.messages


@router.get("/conversations", response_model=List[UUID])
async def get_all_conversations() -> List[UUID]:
    """
    メモリに保存されている全ての会話IDを取得する
    """
    return await get_all_conversation_ids()
