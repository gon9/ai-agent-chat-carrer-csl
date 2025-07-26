import { useState, useEffect } from 'react';
import Head from 'next/head';
import ChatInterface from '../components/ChatInterface';

export default function Home() {
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // 初期表示の準備が完了したことを示す状態
  // 会話IDは最初のメッセージ送信時に自動的に取得される

  // メッセージ送信
  const handleSendMessage = async (message) => {
    if (!message.trim()) return;
    
    // ユーザーメッセージを追加
    const userMessage = { role: 'user', content: message };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    
    setLoading(true);
    
    try {
      const response = await fetch('/api/v1/chat/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: message,
          conversation_id: conversationId
        }),
      });
      
      if (!response.ok) {
        throw new Error('メッセージの送信に失敗しました');
      }
      
      const data = await response.json();
      
      // 会話IDを設定
      setConversationId(data.conversation_id);
      
      // 完全な会話履歴を取得した場合はそれを使用
      if (data.messages && data.messages.length > 0) {
        setMessages(data.messages.map(msg => ({
          role: msg.role,
          content: msg.content
        })));
      } else {
        // 旧エンドポイントとの互換性のため
        setMessages((prevMessages) => [...prevMessages, { 
          role: 'assistant', 
          content: data.message 
        }]);
      }
    } catch (error) {
      console.error('送信エラー:', error);
      setMessages((prevMessages) => [...prevMessages, { 
        role: 'system', 
        content: 'エラーが発生しました。もう一度お試しください。' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>キャリアカウンセラーAIチャット</title>
        <meta name="description" content="キャリアに関する相談ができるAIチャットです" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <main>
        <ChatInterface
          messages={messages}
          onSendMessage={handleSendMessage}
          loading={loading}
        />
      </main>
    </>
  );
}
