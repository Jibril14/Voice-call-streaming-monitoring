import { useState, useEffect, useRef } from 'react';

interface StreamMessage {
  customer?: {
    speaker: string;
    text: string;
    start: number;
    end: number;
    score: number;
  };
  agent?: {
    speaker: string;
    text: string;
    start: number;
    end: number;
    score: number;
  };
}

interface TranscriptEntry {
  role: "agent" | "user";
  content: string;
  words: Array<{ word: string; start: number; end: number }>;
  "sentiment score": number;
}

export const useCallStream = () => {
  const [transcriptObject, setTranscriptObject] = useState<TranscriptEntry[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/stream');
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('Connected to WebSocket');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data: StreamMessage = JSON.parse(event.data);
        console.log('Received data:', data);

        setTranscriptObject((prev) => {
          const newEntries: TranscriptEntry[] = [];

          // Process customer message
          if (data.customer && Object.keys(data.customer).length > 0) {
            newEntries.push({
              role: "user",
              content: data.customer.text,
              words: [{ word: data.customer.text, start: data.customer.start, end: data.customer.end }],
              "sentiment score": data.customer.score
            });
          }

          // Process agent message
          if (data.agent && Object.keys(data.agent).length > 0) {
            newEntries.push({
              role: "agent",
              content: data.agent.text,
              words: [{ word: data.agent.text, start: data.agent.start, end: data.agent.end }],
              "sentiment score": data.agent.score
            });
          }

          return [...prev, ...newEntries];
        });
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return { transcriptObject, isConnected };
};
