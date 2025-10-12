import Navigation from "@/components/Navigation";
import CallDetailsCard from "@/components/CallDetailsCard";
import SentimentChart from "@/components/SentimentChart";
import TranscriptView from "@/components/TranscriptView";
import CallAnalysisCard from "@/components/CallAnalysisCard";

// Sample data matching the provided structure
const sampleCallData = {
  call_id: "Jabr9TXYYJHfvl6Syypi88rdAHYHmcq6",
  agent_id: "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD",
  retell_llm_dynamic_variables: {
    customer_name: "Abdul Samad"
  },
  start_timestamp: 1703302407333,
  end_timestamp: 1703302428855,
  duration_ms: 21522,
  transcript_object: [
    {
      role: "agent" as const,
      content: "Hello! Thank you for calling. How may I assist you today?",
      words: [
        { word: "Hello", start: 0.5, end: 0.9 },
        { word: "Thank", start: 1.0, end: 1.2 },
        { word: "you", start: 1.3, end: 1.5 }
      ],
      "sentiment score": 0.85
    },
    {
      role: "user" as const,
      content: "Hi, I'm calling about my recent order. I'm a bit concerned.",
      words: [
        { word: "Hi", start: 2.1, end: 2.4 },
        { word: "I'm", start: 2.5, end: 2.7 },
        { word: "calling", start: 2.8, end: 3.2 }
      ],
      "sentiment score": 0.45
    },
    {
      role: "agent" as const,
      content: "I completely understand your concern. Let me help you with that right away. Could you please provide me with your order number?",
      words: [
        { word: "I", start: 3.8, end: 3.9 },
        { word: "completely", start: 4.0, end: 4.5 }
      ],
      "sentiment score": 0.82
    },
    {
      role: "user" as const,
      content: "Sure, it's order number 12345. I ordered it last week but haven't received any updates.",
      words: [
        { word: "Sure", start: 5.2, end: 5.5 },
        { word: "it's", start: 5.6, end: 5.8 }
      ],
      "sentiment score": 0.52
    },
    {
      role: "agent" as const,
      content: "Thank you for that information. Let me check the status for you. One moment please.",
      words: [
        { word: "Thank", start: 6.5, end: 6.8 },
        { word: "you", start: 6.9, end: 7.1 }
      ],
      "sentiment score": 0.88
    },
    {
      role: "user" as const,
      content: "Okay, thank you.",
      words: [
        { word: "Okay", start: 8.2, end: 8.5 },
        { word: "thank", start: 8.6, end: 8.9 }
      ],
      "sentiment score": 0.65
    },
    {
      role: "agent" as const,
      content: "Good news! I can see your order is currently in transit and should arrive within 2-3 business days. You'll receive a tracking email shortly.",
      words: [
        { word: "Good", start: 10.1, end: 10.3 },
        { word: "news", start: 10.4, end: 10.7 }
      ],
      "sentiment score": 0.92
    },
    {
      role: "user" as const,
      content: "Oh that's wonderful! I was worried something went wrong. Thank you so much for checking!",
      words: [
        { word: "Oh", start: 11.5, end: 11.7 },
        { word: "that's", start: 11.8, end: 12.0 }
      ],
      "sentiment score": 0.95
    },
    {
      role: "agent" as const,
      content: "You're very welcome! Is there anything else I can help you with today?",
      words: [
        { word: "You're", start: 13.2, end: 13.5 },
        { word: "very", start: 13.6, end: 13.9 }
      ],
      "sentiment score": 0.89
    },
    {
      role: "user" as const,
      content: "No, that's all. You've been really helpful. Have a great day!",
      words: [
        { word: "No", start: 14.8, end: 15.0 },
        { word: "that's", start: 15.1, end: 15.3 }
      ],
      "sentiment score": 0.93
    }
  ],
  call_analysis: {
    call_summary: "The agent successfully assisted the customer with their order inquiry. The customer initially expressed concern about their recent order (order #12345) placed last week without updates. The agent professionally checked the order status and provided positive news that the order is in transit with an expected delivery in 2-3 business days. The customer's sentiment improved significantly throughout the call, ending on a very positive note with appreciation for the assistance.",
    Overall_sentiment: "Positive"
  }
};

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <main className="container mx-auto px-6 py-8">
        <div className="space-y-6">
          <CallDetailsCard
            callId={sampleCallData.call_id}
            agentId={sampleCallData.agent_id}
            customerName={sampleCallData.retell_llm_dynamic_variables.customer_name}
            startTimestamp={sampleCallData.start_timestamp}
            endTimestamp={sampleCallData.end_timestamp}
            durationMs={sampleCallData.duration_ms}
            overallSentiment={sampleCallData.call_analysis.Overall_sentiment}
          />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SentimentChart transcriptObject={sampleCallData.transcript_object} />
            <TranscriptView transcriptObject={sampleCallData.transcript_object} />
          </div>

          <CallAnalysisCard callSummary={sampleCallData.call_analysis.call_summary} />
        </div>
      </main>
    </div>
  );
};

export default Index;
