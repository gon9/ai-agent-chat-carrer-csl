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
    message: str = Field(..., description="ユーザーからのメッセージ、空やデフォルト値は使用できません", example="キャリアについて相談したいです")
    conversation_id: Optional[UUID] = Field(None, description="会話ID、新規会話の場合はNull")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="追加メタデータ情報")


class ChatResponse(BaseModel):
    """
    AIからのチャットレスポンス
    """
    message: str
    conversation_id: UUID
    messages: Optional[List[ChatMessage]] = None
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
