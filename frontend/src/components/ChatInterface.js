import { useState, useRef, useEffect } from 'react';
import styles from '../styles/ChatInterface.module.css';

export default function ChatInterface({ messages, onSendMessage, loading }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  
  // 新しいメッセージが来たらスクロール
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>
        <h1>キャリアカウンセラーAI</h1>
        <p>あなたのキャリアに関する質問や相談に答えます</p>
      </div>
      
      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.welcome}>
            <h2>ようこそ！</h2>
            <p>キャリアに関する質問や悩みを入力してください。</p>
            <p>例：</p>
            <ul>
              <li>「IT業界に転職するにはどうしたらいいですか？」</li>
              <li>「プログラミングのキャリアを始めるにはどの言語がおすすめですか？」</li>
              <li>「履歴書の書き方のアドバイスをください」</li>
            </ul>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div 
              key={index} 
              className={`${styles.message} ${
                msg.role === 'user' ? styles.userMessage : 
                msg.role === 'assistant' ? styles.assistantMessage : 
                styles.systemMessage
              }`}
            >
              <div className={styles.messageContent}>
                {msg.content}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className={`${styles.message} ${styles.assistantMessage}`}>
            <div className={styles.typingIndicator}>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className={styles.inputForm} onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="メッセージを入力..."
          disabled={loading}
          className={styles.inputField}
        />
        <button 
          type="submit" 
          disabled={!input.trim() || loading}
          className={styles.sendButton}
        >
          送信
        </button>
      </form>
    </div>
  );
}
