from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime


class ChatMessage(BaseModel):
    """
    チャットメッセージのスキーマ
    """
    id: UUID = Field(default_factory=uuid4)
    role: str  # 'user' または 'assistant'
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """
    ユーザーからのチャットリクエスト
    """
    message: str
    conversation_id: Optional[UUID] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """
    AIからのチャットレスポンス
    """
    message: str
    conversation_id: UUID
    metadata: Optional[Dict[str, Any]] = None


class Conversation(BaseModel):
    """
    会話履歴
    """
    id: UUID = Field(default_factory=uuid4)
    messages: List[ChatMessage] = []
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
