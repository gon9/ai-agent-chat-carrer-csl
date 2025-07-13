from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from uuid import UUID
from app.schemas.chat import ChatRequest, ChatResponse, Conversation, ChatMessage
from app.services.conversation import handle_chat_request, get_conversation, create_conversation

router = APIRouter()


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest) -> dict:
    """
    ユーザーからのメッセージを受け取り、AIの応答を返す
    """
    try:
        response = await handle_chat_request(
            message=request.message,
            conversation_id=request.conversation_id,
            metadata=request.metadata
        )
        
        return ChatResponse(
            message=response["message"],
            conversation_id=response["conversation_id"],
            metadata=response.get("metadata")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"メッセージの処理中にエラーが発生しました: {str(e)}")


@router.post("/conversations", response_model=Conversation)
async def create_new_conversation() -> Conversation:
    """
    新しい会話を作成する
    """
    try:
        conversation = await create_conversation()
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"会話の作成中にエラーが発生しました: {str(e)}")


@router.get("/conversations/{conversation_id}", response_model=Optional[Conversation])
async def get_conversation_by_id(conversation_id: UUID) -> Optional[Conversation]:
    """
    指定されたIDの会話を取得する
    """
    conversation = await get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail=f"ID {conversation_id} の会話が見つかりません")
    return conversation


@router.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessage])
async def get_conversation_messages(conversation_id: UUID) -> List[ChatMessage]:
    """
    指定された会話のメッセージを取得する
    """
    conversation = await get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail=f"ID {conversation_id} の会話が見つかりません")
    return conversation.messages
