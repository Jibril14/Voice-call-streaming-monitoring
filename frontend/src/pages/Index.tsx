import Navigation from "@/components/Navigation";
import CallDetailsCard from "@/components/CallDetailsCard";
import SentimentChart from "@/components/SentimentChart";
import TranscriptView from "@/components/TranscriptView";
import CallAnalysisCard from "@/components/CallAnalysisCard";
import { useCallStream } from "@/hooks/useCallStream";
import { useMemo, useState } from "react";
import { toast } from "sonner";

interface CallDetails {
  CallID: string;
  Customer: string;
  Duration: string;
  StartTime: string;
}

const Index = () => {
  const { transcriptObject, isConnected } = useCallStream();
  const [callDetails, setCallDetails] = useState<CallDetails | null>(null);
  const [isStartingCall, setIsStartingCall] = useState(false);

  const handleMakeCall = () => {
    // Set flag and reload first
    localStorage.setItem("makeCall", "true");
    window.location.reload();
  };

  // Make POST request after reload if flag is set
  useState(() => {
    const shouldMakeCall = localStorage.getItem("makeCall");
    if (shouldMakeCall === "true") {
      localStorage.removeItem("makeCall");
      setIsStartingCall(true);
      
      fetch("http://localhost:8000/start-call", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error("Failed to start call");
          }
          return response.json();
        })
        .then(data => {
          setCallDetails(data.CallDetails);
          setIsStartingCall(false);
        })
        .catch(error => {
          console.error("Error starting call:", error);
          toast.error("Failed to start call");
          setIsStartingCall(false);
        });
    }
  });

  const callSummary = useMemo(() => {
    return transcriptObject.map(entry => entry.content).join(' ');
  }, [transcriptObject]);

  const startTimestamp = useMemo(() => {
    return transcriptObject.length > 0 && transcriptObject[0].words.length > 0
      ? Date.now() - (transcriptObject[0].words[0].start * 1000)
      : Date.now();
  }, [transcriptObject]);

  const endTimestamp = useMemo(() => {
    return Date.now();
  }, [transcriptObject]);

  const durationMs = useMemo(() => {
    if (transcriptObject.length === 0) return 0;
    const lastEntry = transcriptObject[transcriptObject.length - 1];
    if (lastEntry.words.length === 0) return 0;
    return (lastEntry.words[lastEntry.words.length - 1].end * 1000);
  }, [transcriptObject]);

  const overallSentiment = useMemo(() => {
    if (transcriptObject.length === 0) return "Neutral";
    const avgScore = transcriptObject.reduce((sum, entry) => sum + entry["sentiment score"], 0) / transcriptObject.length;
    if (avgScore >= 0.7) return "Positive";
    if (avgScore >= 0.4) return "Neutral";
    return "Negative";
  }, [transcriptObject]);

  return (
    <div className="min-h-screen bg-background">
      <Navigation onMakeCall={handleMakeCall} isLoading={isStartingCall} />
      
      <main className="container mx-auto px-6 py-8">
        <div className="space-y-6">
          {callDetails && (
            <CallDetailsCard
              callId={callDetails.CallID}
              agentId="real-time-agent"
              customerName={callDetails.Customer}
              startTimestamp={new Date(callDetails.StartTime).getTime()}
              endTimestamp={endTimestamp}
              durationMs={durationMs}
              overallSentiment={overallSentiment}
            />
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SentimentChart transcriptObject={transcriptObject} />
            <TranscriptView transcriptObject={transcriptObject} />
          </div>

          <CallAnalysisCard callSummary={callSummary || "Waiting for call data..."} />
        </div>
      </main>
    </div>
  );
};

export default Index;
