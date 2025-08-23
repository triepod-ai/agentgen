# React WebSocket Component - Enterprise Edge Case Solution

A comprehensive React component that handles the complex intersection of real-time WebSocket data streams, server-side rendering, React 18 concurrent features, error boundaries, and Next.js App/Pages Router compatibility.

## 🎯 Edge Cases Handled

### ✅ Real-time WebSocket Data Streams
- **Automatic reconnection** with exponential backoff
- **Message queuing** and overflow protection (configurable max messages)
- **Connection state management** (connecting, connected, disconnected, error)
- **Protocol support** for WebSocket subprotocols
- **Memory optimization** with message limits and cleanup

### ✅ Server-Side Rendering (SSR)
- **SSR detection** and graceful fallback
- **Hydration safety** - no WebSocket creation on server
- **Fallback components** for server-rendered content
- **Progressive enhancement** approach

### ✅ React 18 Concurrent Features
- **startTransition** for non-urgent state updates
- **useDeferredValue** for performance optimization
- **Concurrent rendering** compatible state management
- **Automatic batching** support

### ✅ Error Boundaries for WebSocket Failures
- **Dedicated WebSocket error boundary** class component
- **Graceful error recovery** with retry mechanisms
- **Custom fallback UI** support
- **Error logging** and reporting callbacks

### ✅ Next.js App Router & Pages Router
- **Universal compatibility** with both routing systems
- **getServerSideProps** integration for Pages Router
- **App Router** server component compatibility
- **Environment detection** and adaptation

## 🏗️ Architecture

### Core Components

1. **WebSocketStream** - Main component with render props pattern
2. **WebSocketErrorBoundary** - Specialized error boundary for WebSocket failures
3. **useWebSocket** - Custom hook for WebSocket management
4. **WebSocketProvider** - Context provider for multiple connections
5. **withWebSocket** - Higher-order component wrapper

### Key Features

- **TypeScript-first** with comprehensive type definitions
- **Performance optimized** with React 18 concurrent features
- **Memory safe** with automatic cleanup and limits
- **Accessibility ready** with proper ARIA attributes
- **Mobile responsive** with adaptive layouts
- **Dark mode support** via CSS custom properties

## 📋 API Reference

### WebSocketStream Props

```typescript
interface WebSocketStreamProps {
  url: string;                                    // WebSocket URL
  protocols?: string | string[];                  // WebSocket protocols
  onMessage?: (message: WebSocketMessage) => void;
  onError?: (error: Event | Error) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  reconnectAttempts?: number;                     // Default: 3
  reconnectDelay?: number;                        // Default: 1000ms
  maxMessages?: number;                           // Default: 1000
  enableSSR?: boolean;                            // Default: true
  fallbackComponent?: ReactNode;
  children?: (props: RenderProps) => ReactNode;
}
```

### Render Props Interface

```typescript
interface RenderProps {
  messages: WebSocketMessage[];
  connectionState: 'connecting' | 'connected' | 'disconnected' | 'error';
  sendMessage: (data: any) => void;
  reconnect: () => void;
}
```

## 🚀 Usage Examples

### Basic Usage

```tsx
import { WebSocketStream } from './WebSocketStream';

export const BasicExample = () => (
  <WebSocketStream url="wss://echo.websocket.org">
    {({ messages, connectionState, sendMessage }) => (
      <div>
        <h2>Status: {connectionState}</h2>
        <div>
          {messages.map(msg => (
            <div key={msg.id}>{JSON.stringify(msg.data)}</div>
          ))}
        </div>
        <button onClick={() => sendMessage({ hello: 'world' })}>
          Send Message
        </button>
      </div>
    )}
  </WebSocketStream>
);
```

### Next.js App Router

```tsx
// app/dashboard/page.tsx
import { WebSocketStream } from './WebSocketStream';

export default function DashboardPage() {
  return (
    <div>
      <h1>Real-time Dashboard</h1>
      <WebSocketStream
        url="wss://api.example.com/realtime"
        protocols={['v1.0.protocol']}
        maxMessages={500}
        fallbackComponent={<div>Loading...</div>}
      >
        {({ messages, connectionState, sendMessage }) => (
          <div className="dashboard">
            <header>Status: {connectionState}</header>
            <main>
              {messages.map(msg => (
                <div key={msg.id} className="data-card">
                  {JSON.stringify(msg.data)}
                </div>
              ))}
            </main>
          </div>
        )}
      </WebSocketStream>
    </div>
  );
}
```

### Next.js Pages Router with SSR

```tsx
// pages/realtime.tsx
import { WebSocketStream } from '../components/WebSocketStream';

export async function getServerSideProps() {
  return {
    props: {
      wsUrl: process.env.WEBSOCKET_URL || 'wss://api.example.com/realtime',
    },
  };
}

export default function RealtimePage({ wsUrl }: { wsUrl: string }) {
  return (
    <WebSocketStream
      url={wsUrl}
      enableSSR={true}
      fallbackComponent={
        <div className="ssr-loading">
          Establishing connection...
        </div>
      }
    >
      {({ messages, connectionState, sendMessage }) => (
        <div>
          <h1>Live Data</h1>
          <span className={`status ${connectionState}`}>
            {connectionState}
          </span>
          {messages.map(msg => (
            <div key={msg.id}>{JSON.stringify(msg.data)}</div>
          ))}
        </div>
      )}
    </WebSocketStream>
  );
}
```

### React 18 Concurrent Features

```tsx
import React, { Suspense } from 'react';
import { WebSocketStream } from './WebSocketStream';

const ConcurrentExample = () => (
  <Suspense fallback={<div>Loading...</div>}>
    <WebSocketStream url="wss://api.example.com/concurrent">
      {({ messages, connectionState, sendMessage }) => (
        <div>
          {/* React 18 will batch these updates automatically */}
          <h2>Connection: {connectionState}</h2>
          <div className="data-stream">
            {messages.map(message => (
              <React.memo(DataItem)({ key: message.id, message })
            ))}
          </div>
          <button onClick={() => sendMessage({ request: 'data' })}>
            Request Data
          </button>
        </div>
      )}
    </WebSocketStream>
  </Suspense>
);
```

### Error Handling with Custom Fallback

```tsx
const ErrorHandlingExample = () => {
  const customErrorFallback = (
    <div className="error-fallback">
      <h3>Connection Failed</h3>
      <p>Unable to establish WebSocket connection.</p>
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
      onError={(error) => console.error('WebSocket error:', error)}
    >
      {({ messages, connectionState, reconnect }) => (
        <div>
          <h2>Reliable Connection</h2>
          {connectionState === 'error' && (
            <button onClick={reconnect}>Retry Connection</button>
          )}
          {messages.map(msg => (
            <div key={msg.id}>{JSON.stringify(msg.data)}</div>
          ))}
        </div>
      )}
    </WebSocketStream>
  );
};
```

### Multiple WebSocket Connections

```tsx
import { WebSocketProvider, useWebSocketContext } from './WebSocketStream';

const MultiConnectionDashboard = () => {
  const { addConnection, sendToConnection, connectionStates } = 
    useWebSocketContext();

  React.useEffect(() => {
    addConnection('feed1', 'wss://feed1.example.com/data');
    addConnection('feed2', 'wss://feed2.example.com/data');
  }, [addConnection]);

  return (
    <div>
      <h1>Multi-Connection Dashboard</h1>
      {Array.from(connectionStates.entries()).map(([key, state]) => (
        <div key={key} className={`connection ${state}`}>
          {key}: {state}
        </div>
      ))}
      <button onClick={() => sendToConnection('feed1', { action: 'subscribe' })}>
        Subscribe to Feed 1
      </button>
    </div>
  );
};

// Wrap with provider
export const App = () => (
  <WebSocketProvider>
    <MultiConnectionDashboard />
  </WebSocketProvider>
);
```

### Higher-Order Component Pattern

```tsx
const ChatComponent = withWebSocket(
  ({ messages, sendMessage, connectionState }) => {
    const [input, setInput] = React.useState('');
    
    const handleSend = () => {
      if (input.trim()) {
        sendMessage({
          type: 'message',
          text: input,
          timestamp: Date.now(),
        });
        setInput('');
      }
    };

    return (
      <div className="chat">
        <div className="messages">
          {messages.map(msg => (
            <div key={msg.id}>{msg.data.text}</div>
          ))}
        </div>
        <div className="input">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            disabled={connectionState !== 'connected'}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    );
  },
  {
    url: 'wss://chat.example.com/socket',
    protocols: ['chat-v1'],
    options: { reconnectAttempts: 10 },
  }
);
```

## 🎨 Styling

The component includes comprehensive CSS with:

- **Responsive design** for mobile and desktop
- **Dark mode support** via CSS custom properties
- **High contrast mode** accessibility
- **Reduced motion** support
- **Loading states** and transitions
- **Connection status indicators**

Import the CSS module:

```tsx
import styles from './WebSocketStream.module.css';

<WebSocketStream className={styles.customTheme} url="...">
  {/* ... */}
</WebSocketStream>
```

## 🔧 Advanced Configuration

### Custom Reconnection Logic

```tsx
<WebSocketStream
  url="wss://api.example.com/socket"
  reconnectAttempts={5}
  reconnectDelay={2000}  // Initial delay
  // Exponential backoff: 2s, 4s, 8s, 16s, 32s
  onError={(error) => {
    // Custom error handling
    if (error instanceof CloseEvent && error.code === 1006) {
      // Handle abnormal closure
      console.log('Connection lost unexpectedly');
    }
  }}
/>
```

### Message Filtering and Processing

```tsx
<WebSocketStream
  url="wss://api.example.com/socket"
  maxMessages={100}
  onMessage={(message) => {
    // Process messages before state update
    if (message.data.type === 'heartbeat') {
      // Don't store heartbeat messages
      return;
    }
    // Store in external state manager if needed
    store.dispatch(addMessage(message));
  }}
>
  {({ messages }) => (
    <div>
      {/* Only display non-heartbeat messages */}
      {messages
        .filter(msg => msg.data.type !== 'heartbeat')
        .map(msg => (
          <div key={msg.id}>{JSON.stringify(msg.data)}</div>
        ))}
    </div>
  )}
</WebSocketStream>
```

## 🧪 Testing

The component is designed for easy testing:

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { WebSocketStream } from './WebSocketStream';

// Mock WebSocket for testing
class MockWebSocket {
  constructor(public url: string) {}
  close = jest.fn();
  send = jest.fn();
  addEventListener = jest.fn();
  removeEventListener = jest.fn();
}

global.WebSocket = MockWebSocket as any;

test('renders fallback on server', () => {
  // Simulate server environment
  delete (global as any).window;
  
  render(
    <WebSocketStream 
      url="wss://test.com" 
      fallbackComponent={<div>Server fallback</div>}
    />
  );
  
  expect(screen.getByText('Server fallback')).toBeInTheDocument();
});

test('handles connection errors gracefully', async () => {
  const onError = jest.fn();
  
  render(
    <WebSocketStream url="wss://invalid.com" onError={onError}>
      {({ connectionState }) => <div>Status: {connectionState}</div>}
    </WebSocketStream>
  );
  
  // Simulate connection error
  const ws = MockWebSocket.mock.instances[0];
  ws.onerror(new Event('error'));
  
  await waitFor(() => {
    expect(screen.getByText('Status: error')).toBeInTheDocument();
  });
});
```

## 🚀 Performance Considerations

1. **Memory Management**: Automatic message limit and cleanup
2. **React 18 Optimization**: Uses concurrent features for smooth rendering
3. **Reconnection Strategy**: Exponential backoff prevents server overwhelm
4. **Bundle Size**: Tree-shakeable with minimal dependencies
5. **SSR Compatible**: No hydration mismatches

## 🔒 Security Notes

- Always use WSS (secure WebSocket) in production
- Validate all incoming messages before processing
- Implement rate limiting on the server side
- Consider authentication tokens for WebSocket connections
- Sanitize any user-generated content before display

## 📚 Files Created

1. **WebSocketStream.tsx** - Main component with all features
2. **WebSocketStream.module.css** - Comprehensive styling
3. **WebSocketProvider.tsx** - Context provider for multiple connections
4. **usage-examples.tsx** - Comprehensive usage examples
5. **README-WebSocket.md** - This documentation

This solution handles all the complex edge cases while maintaining clean, performant, and maintainable code that works across all React and Next.js environments.