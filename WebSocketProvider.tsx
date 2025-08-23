import React, { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

// Context for managing multiple WebSocket connections across the app
interface WebSocketContextValue {
  connections: Map<string, WebSocket>;
  addConnection: (key: string, url: string, protocols?: string | string[]) => void;
  removeConnection: (key: string) => void;
  getConnection: (key: string) => WebSocket | undefined;
  sendToConnection: (key: string, data: any) => boolean;
  connectionStates: Map<string, 'connecting' | 'connected' | 'disconnected' | 'error'>;
}

const WebSocketContext = createContext<WebSocketContextValue | null>(null);

interface WebSocketProviderProps {
  children: ReactNode;
  globalConfig?: {
    reconnectAttempts?: number;
    reconnectDelay?: number;
    heartbeatInterval?: number;
  };
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
  globalConfig = {},
}) => {
  const [connections] = useState(() => new Map<string, WebSocket>());
  const [connectionStates, setConnectionStates] = useState(
    () => new Map<string, 'connecting' | 'connected' | 'disconnected' | 'error'>()
  );

  const addConnection = (key: string, url: string, protocols?: string | string[]) => {
    // Close existing connection if it exists
    const existingConnection = connections.get(key);
    if (existingConnection) {
      existingConnection.close();
    }

    try {
      const ws = new WebSocket(url, protocols);
      
      setConnectionStates(prev => new Map(prev).set(key, 'connecting'));

      ws.onopen = () => {
        setConnectionStates(prev => new Map(prev).set(key, 'connected'));
      };

      ws.onerror = () => {
        setConnectionStates(prev => new Map(prev).set(key, 'error'));
      };

      ws.onclose = () => {
        setConnectionStates(prev => new Map(prev).set(key, 'disconnected'));
        connections.delete(key);
      };

      connections.set(key, ws);
    } catch (error) {
      console.error(`Failed to create WebSocket connection for ${key}:`, error);
      setConnectionStates(prev => new Map(prev).set(key, 'error'));
    }
  };

  const removeConnection = (key: string) => {
    const connection = connections.get(key);
    if (connection) {
      connection.close();
      connections.delete(key);
      setConnectionStates(prev => {
        const newStates = new Map(prev);
        newStates.delete(key);
        return newStates;
      });
    }
  };

  const getConnection = (key: string) => {
    return connections.get(key);
  };

  const sendToConnection = (key: string, data: any): boolean => {
    const connection = connections.get(key);
    if (connection && connection.readyState === WebSocket.OPEN) {
      try {
        connection.send(JSON.stringify(data));
        return true;
      } catch (error) {
        console.error(`Failed to send data to connection ${key}:`, error);
        return false;
      }
    }
    return false;
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      connections.forEach((ws) => {
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          ws.close();
        }
      });
      connections.clear();
    };
  }, [connections]);

  const contextValue: WebSocketContextValue = {
    connections,
    addConnection,
    removeConnection,
    getConnection,
    sendToConnection,
    connectionStates,
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocketContext must be used within a WebSocketProvider');
  }
  return context;
};