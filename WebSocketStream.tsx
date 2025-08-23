import React, {
  useState,
  useEffect,
  useRef,
  useCallback,
  useMemo,
  startTransition,
  useDeferredValue,
  type ReactNode,
  type ComponentPropsWithoutRef,
} from 'react';

// Types for the component
interface WebSocketMessage {
  id: string;
  timestamp: number;
  data: any;
  type?: string;
}

interface WebSocketStreamProps extends ComponentPropsWithoutRef<'div'> {
  url: string;
  protocols?: string | string[];
  onMessage?: (message: WebSocketMessage) => void;
  onError?: (error: Event | Error) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  reconnectAttempts?: number;
  reconnectDelay?: number;
  maxMessages?: number;
  enableSSR?: boolean;
  fallbackComponent?: ReactNode;
  children?: (props: {
    messages: WebSocketMessage[];
    connectionState: 'connecting' | 'connected' | 'disconnected' | 'error';
    sendMessage: (data: any) => void;
    reconnect: () => void;
  }) => ReactNode;
}

interface WebSocketError extends Error {
  code?: number;
  reason?: string;
  wasClean?: boolean;
}

// Error boundary specifically for WebSocket failures
class WebSocketErrorBoundary extends React.Component<
  {
    children: ReactNode;
    fallback?: ReactNode;
    onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
  },
  { hasError: boolean; error?: Error }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('WebSocket Error Boundary caught an error:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="websocket-error">
            <h3>WebSocket Connection Error</h3>
            <p>Failed to establish or maintain WebSocket connection.</p>
            <button
              onClick={() => this.setState({ hasError: false, error: undefined })}
            >
              Retry Connection
            </button>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

// Custom hook for WebSocket management with SSR support
function useWebSocket(
  url: string,
  options: {
    protocols?: string | string[];
    onMessage?: (message: WebSocketMessage) => void;
    onError?: (error: Event | Error) => void;
    onConnect?: () => void;
    onDisconnect?: () => void;
    reconnectAttempts?: number;
    reconnectDelay?: number;
    enableSSR?: boolean;
  } = {}
) {
  const {
    protocols,
    onMessage,
    onError,
    onConnect,
    onDisconnect,
    reconnectAttempts = 3,
    reconnectDelay = 1000,
    enableSSR = true,
  } = options;

  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [connectionState, setConnectionState] = useState<
    'connecting' | 'connected' | 'disconnected' | 'error'
  >('disconnected');

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCountRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  const isMountedRef = useRef(true);

  // SSR detection
  const isServer = typeof window === 'undefined';
  const isClient = !isServer;

  // Deferred values for React 18 concurrent features
  const deferredMessages = useDeferredValue(messages);
  const deferredConnectionState = useDeferredValue(connectionState);

  const connect = useCallback(() => {
    // Skip WebSocket creation on server-side or if already connected
    if (isServer || wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      setConnectionState('connecting');
      
      const ws = new WebSocket(url, protocols);
      wsRef.current = ws;

      ws.onopen = () => {
        if (!isMountedRef.current) return;
        
        startTransition(() => {
          setConnectionState('connected');
          reconnectCountRef.current = 0;
        });
        onConnect?.();
      };

      ws.onmessage = (event) => {
        if (!isMountedRef.current) return;

        try {
          const parsedData = JSON.parse(event.data);
          const message: WebSocketMessage = {
            id: crypto.randomUUID?.() || `${Date.now()}-${Math.random()}`,
            timestamp: Date.now(),
            data: parsedData,
            type: parsedData.type,
          };

          startTransition(() => {
            setMessages((prev) => [...prev, message]);
          });
          
          onMessage?.(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
          onError?.(error as Error);
        }
      };

      ws.onerror = (error) => {
        if (!isMountedRef.current) return;
        
        startTransition(() => {
          setConnectionState('error');
        });
        onError?.(error);
      };

      ws.onclose = (event) => {
        if (!isMountedRef.current) return;

        startTransition(() => {
          setConnectionState('disconnected');
        });
        onDisconnect?.();

        // Auto-reconnect logic
        if (
          !event.wasClean &&
          reconnectCountRef.current < reconnectAttempts &&
          isMountedRef.current
        ) {
          reconnectCountRef.current++;
          reconnectTimeoutRef.current = setTimeout(() => {
            if (isMountedRef.current) {
              connect();
            }
          }, reconnectDelay * Math.pow(2, reconnectCountRef.current - 1)); // Exponential backoff
        }
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      setConnectionState('error');
      onError?.(error as Error);
    }
  }, [url, protocols, onMessage, onError, onConnect, onDisconnect, reconnectAttempts, reconnectDelay]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (wsRef.current) {
      wsRef.current.close(1000, 'User initiated disconnect');
      wsRef.current = null;
    }
    
    startTransition(() => {
      setConnectionState('disconnected');
    });
  }, []);

  const sendMessage = useCallback((data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      try {
        wsRef.current.send(JSON.stringify(data));
      } catch (error) {
        console.error('Failed to send WebSocket message:', error);
        onError?.(error as Error);
      }
    } else {
      console.warn('WebSocket is not connected. Cannot send message.');
    }
  }, [onError]);

  const reconnect = useCallback(() => {
    disconnect();
    reconnectCountRef.current = 0;
    setTimeout(connect, 100);
  }, [connect, disconnect]);

  // Effect for managing connection lifecycle
  useEffect(() => {
    isMountedRef.current = true;

    // Only connect on client-side
    if (isClient) {
      connect();
    }

    return () => {
      isMountedRef.current = false;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      disconnect();
    };
  }, [connect, disconnect, isClient]);

  // Return deferred values for better concurrent rendering
  return {
    messages: deferredMessages,
    connectionState: deferredConnectionState,
    sendMessage,
    reconnect,
    isConnected: deferredConnectionState === 'connected',
    isServer,
  };
}

// Main WebSocket component
export const WebSocketStream: React.FC<WebSocketStreamProps> = ({
  url,
  protocols,
  onMessage,
  onError,
  onConnect,
  onDisconnect,
  reconnectAttempts = 3,
  reconnectDelay = 1000,
  maxMessages = 1000,
  enableSSR = true,
  fallbackComponent,
  children,
  className,
  ...rest
}) => {
  const {
    messages: allMessages,
    connectionState,
    sendMessage,
    reconnect,
    isServer,
  } = useWebSocket(url, {
    protocols,
    onMessage,
    onError,
    onConnect,
    onDisconnect,
    reconnectAttempts,
    reconnectDelay,
    enableSSR,
  });

  // Limit messages to prevent memory issues
  const messages = useMemo(() => {
    return allMessages.slice(-maxMessages);
  }, [allMessages, maxMessages]);

  // SSR fallback
  if (isServer && enableSSR) {
    return (
      <div className={`websocket-stream ssr-fallback ${className || ''}`} {...rest}>
        {fallbackComponent || (
          <div className="loading">
            <p>Initializing WebSocket connection...</p>
          </div>
        )}
      </div>
    );
  }

  const containerProps = {
    messages,
    connectionState,
    sendMessage,
    reconnect,
  };

  return (
    <WebSocketErrorBoundary
      fallback={fallbackComponent}
      onError={(error, errorInfo) => {
        console.error('WebSocket component error:', error, errorInfo);
        onError?.(error);
      }}
    >
      <div
        className={`websocket-stream ${connectionState} ${className || ''}`}
        {...rest}
      >
        {children ? children(containerProps) : (
          <DefaultWebSocketUI {...containerProps} />
        )}
      </div>
    </WebSocketErrorBoundary>
  );
};

// Default UI component
const DefaultWebSocketUI: React.FC<{
  messages: WebSocketMessage[];
  connectionState: string;
  sendMessage: (data: any) => void;
  reconnect: () => void;
}> = ({ messages, connectionState, sendMessage, reconnect }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim()) {
      sendMessage({ message: inputValue, timestamp: Date.now() });
      setInputValue('');
    }
  };

  return (
    <>
      <div className="websocket-status">
        <span className={`status-indicator ${connectionState}`}>
          {connectionState}
        </span>
        {connectionState !== 'connected' && (
          <button onClick={reconnect}>Reconnect</button>
        )}
      </div>

      <div className="websocket-messages">
        {messages.map((message) => (
          <div key={message.id} className="message">
            <span className="timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </span>
            <span className="data">{JSON.stringify(message.data)}</span>
          </div>
        ))}
      </div>

      <div className="websocket-input">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={connectionState !== 'connected'}
          placeholder="Type a message..."
        />
        <button onClick={handleSend} disabled={connectionState !== 'connected'}>
          Send
        </button>
      </div>
    </>
  );
};

// Higher-order component for additional WebSocket features
export const withWebSocket = <P extends object>(
  Component: React.ComponentType<P>,
  wsConfig: {
    url: string;
    protocols?: string | string[];
    options?: Partial<WebSocketStreamProps>;
  }
) => {
  return React.forwardRef<any, P>((props, ref) => {
    const wsProps = useWebSocket(wsConfig.url, {
      protocols: wsConfig.protocols,
      ...wsConfig.options,
    });

    return <Component {...props} {...wsProps} ref={ref} />;
  });
};

export default WebSocketStream;