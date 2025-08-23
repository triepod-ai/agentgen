import React from 'react';
import { WebSocketStream, WebSocketProvider, useWebSocketContext, withWebSocket } from './WebSocketStream';

// Example 1: Basic usage with render props
export const BasicWebSocketExample = () => {
  return (
    <WebSocketStream url="wss://echo.websocket.org">
      {({ messages, connectionState, sendMessage, reconnect }) => (
        <div>
          <h2>WebSocket Connection Status: {connectionState}</h2>
          <div>
            {messages.map(message => (
              <div key={message.id}>
                {new Date(message.timestamp).toLocaleTimeString()}: {JSON.stringify(message.data)}
              </div>
            ))}
          </div>
          <button onClick={() => sendMessage({ hello: 'world' })}>
            Send Test Message
          </button>
          {connectionState !== 'connected' && (
            <button onClick={reconnect}>Reconnect</button>
          )}
        </div>
      )}
    </WebSocketStream>
  );
};

// Example 2: Next.js App Router page component
export default function AppRouterPage() {
  return (
    <WebSocketProvider>
      <div className="container">
        <h1>Real-time Dashboard</h1>
        <WebSocketStream
          url="wss://api.example.com/realtime"
          protocols={['v1.0.protocol']}
          maxMessages={500}
          reconnectAttempts={5}
          reconnectDelay={2000}
          onConnect={() => console.log('Connected to real-time feed')}
          onError={(error) => console.error('WebSocket error:', error)}
          fallbackComponent={
            <div>Loading real-time data feed...</div>
          }
        />
      </div>
    </WebSocketProvider>
  );
}

// Example 3: Next.js Pages Router with getServerSideProps
export async function getServerSideProps() {
  // SSR-compatible - WebSocket will initialize on client
  return {
    props: {
      wsUrl: process.env.WEBSOCKET_URL || 'wss://api.example.com/realtime',
    },
  };
}

export function PagesRouterPage({ wsUrl }: { wsUrl: string }) {
  return (
    <WebSocketProvider>
      <WebSocketStream
        url={wsUrl}
        enableSSR={true}
        fallbackComponent={
          <div className="ssr-fallback">
            <div>Establishing real-time connection...</div>
            <div className="spinner">⏳</div>
          </div>
        }
      >
        {({ messages, connectionState, sendMessage }) => (
          <div>
            <header>
              <h1>Live Data Stream</h1>
              <span className={`status ${connectionState}`}>
                {connectionState.toUpperCase()}
              </span>
            </header>
            
            <main>
              {messages.length === 0 ? (
                <div>Waiting for data...</div>
              ) : (
                <div className="message-grid">
                  {messages.map(msg => (
                    <div key={msg.id} className="message-card">
                      <div className="timestamp">
                        {new Date(msg.timestamp).toLocaleString()}
                      </div>
                      <div className="content">
                        {JSON.stringify(msg.data, null, 2)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </main>
            
            <footer>
              <button 
                onClick={() => sendMessage({ action: 'ping', timestamp: Date.now() })}
                disabled={connectionState !== 'connected'}
              >
                Send Ping
              </button>
            </footer>
          </div>
        )}
      </WebSocketStream>
    </WebSocketProvider>
  );
}

// Example 4: Higher-order component usage
const ChatComponent = withWebSocket(
  ({ messages, sendMessage, connectionState }: any) => {
    const [inputText, setInputText] = React.useState('');

    const handleSend = () => {
      if (inputText.trim()) {
        sendMessage({
          type: 'chat_message',
          text: inputText,
          user: 'current_user',
          timestamp: Date.now(),
        });
        setInputText('');
      }
    };

    return (
      <div className="chat-container">
        <div className="chat-messages">
          {messages
            .filter((msg: any) => msg.data.type === 'chat_message')
            .map((msg: any) => (
              <div key={msg.id} className="chat-message">
                <strong>{msg.data.user}:</strong> {msg.data.text}
              </div>
            ))}
        </div>
        
        <div className="chat-input">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type a message..."
            disabled={connectionState !== 'connected'}
          />
          <button onClick={handleSend} disabled={connectionState !== 'connected'}>
            Send
          </button>
        </div>
      </div>
    );
  },
  {
    url: 'wss://chat.example.com/socket',
    protocols: ['chat-v1'],
    options: {
      reconnectAttempts: 10,
      reconnectDelay: 1000,
    },
  }
);

// Example 5: React 18 Concurrent Features with Suspense
const ConcurrentWebSocketExample = () => {
  return (
    <React.Suspense fallback={<div>Loading WebSocket connection...</div>}>
      <WebSocketStream
        url="wss://api.example.com/concurrent-data"
        maxMessages={1000}
      >
        {({ messages, connectionState, sendMessage }) => (
          <div>
            <h2>Concurrent WebSocket Data</h2>
            <p>Connection: {connectionState}</p>
            
            {/* React 18 concurrent rendering will batch these updates */}
            <div className="data-stream">
              {messages.map(message => (
                <React.memo(({ message }: { message: any }) => (
                  <div key={message.id} className="data-item">
                    <time>{new Date(message.timestamp).toISOString()}</time>
                    <pre>{JSON.stringify(message.data, null, 2)}</pre>
                  </div>
                ))}
              ))}
            </div>
            
            <button onClick={() => sendMessage({ request: 'more_data' })}>
              Request More Data
            </button>
          </div>
        )}
      </WebSocketStream>
    </React.Suspense>
  );
};

// Example 6: Multiple WebSocket connections with context
export const MultipleConnectionsExample = () => {
  const { addConnection, sendToConnection, connectionStates } = useWebSocketContext();

  React.useEffect(() => {
    // Set up multiple connections
    addConnection('feed1', 'wss://feed1.example.com/data');
    addConnection('feed2', 'wss://feed2.example.com/data');
    addConnection('notifications', 'wss://notifications.example.com/socket');
  }, [addConnection]);

  return (
    <div className="multi-connection-dashboard">
      <h1>Multi-Connection Dashboard</h1>
      
      <div className="connection-status">
        {Array.from(connectionStates.entries()).map(([key, state]) => (
          <div key={key} className={`connection-indicator ${state}`}>
            {key}: {state}
          </div>
        ))}
      </div>
      
      <div className="controls">
        <button onClick={() => sendToConnection('feed1', { action: 'subscribe', topic: 'stocks' })}>
          Subscribe to Stocks
        </button>
        <button onClick={() => sendToConnection('feed2', { action: 'subscribe', topic: 'crypto' })}>
          Subscribe to Crypto
        </button>
        <button onClick={() => sendToConnection('notifications', { action: 'enable' })}>
          Enable Notifications
        </button>
      </div>
      
      {/* Individual WebSocket streams for each connection */}
      <div className="feeds-grid">
        <WebSocketStream url="wss://feed1.example.com/data">
          {({ messages }) => (
            <div className="feed-panel">
              <h3>Stock Feed</h3>
              {messages.slice(-10).map(msg => (
                <div key={msg.id}>{JSON.stringify(msg.data)}</div>
              ))}
            </div>
          )}
        </WebSocketStream>
        
        <WebSocketStream url="wss://feed2.example.com/data">
          {({ messages }) => (
            <div className="feed-panel">
              <h3>Crypto Feed</h3>
              {messages.slice(-10).map(msg => (
                <div key={msg.id}>{JSON.stringify(msg.data)}</div>
              ))}
            </div>
          )}
        </WebSocketStream>
      </div>
    </div>
  );
};

// Example 7: Error boundary integration with custom fallback
export const ErrorHandlingExample = () => {
  const [hasError, setHasError] = React.useState(false);

  const customErrorFallback = (
    <div className="websocket-error-fallback">
      <h3>Connection Failed</h3>
      <p>Unable to establish WebSocket connection.</p>
      <details>
        <summary>Troubleshooting</summary>
        <ul>
          <li>Check your internet connection</li>
          <li>Verify the WebSocket URL is correct</li>
          <li>Check if the service is running</li>
          <li>Try refreshing the page</li>
        </ul>
      </details>
      <button onClick={() => window.location.reload()}>
        Reload Page
      </button>
    </div>
  );

  return (
    <WebSocketStream
      url="wss://unreliable-service.example.com/socket"
      reconnectAttempts={3}
      reconnectDelay={5000}
      fallbackComponent={customErrorFallback}
      onError={(error) => {
        console.error('WebSocket error occurred:', error);
        setHasError(true);
      }}
      onConnect={() => {
        setHasError(false);
      }}
    >
      {({ messages, connectionState, sendMessage, reconnect }) => (
        <div>
          <h2>Reliable WebSocket Connection</h2>
          
          {hasError && (
            <div className="error-banner">
              <span>⚠️ Connection issues detected</span>
              <button onClick={reconnect}>Retry</button>
            </div>
          )}
          
          <div className="connection-health">
            Status: <span className={connectionState}>{connectionState}</span>
            {connectionState === 'error' && (
              <button onClick={reconnect}>Manual Reconnect</button>
            )}
          </div>
          
          <div className="message-list">
            {messages.map(message => (
              <div key={message.id} className="message">
                <span className="time">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
                <span className="data">
                  {JSON.stringify(message.data)}
                </span>
              </div>
            ))}
          </div>
          
          <button 
            onClick={() => sendMessage({ heartbeat: Date.now() })}
            disabled={connectionState !== 'connected'}
          >
            Send Heartbeat
          </button>
        </div>
      )}
    </WebSocketStream>
  );
};