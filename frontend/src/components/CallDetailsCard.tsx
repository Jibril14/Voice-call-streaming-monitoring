import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock, User, Phone, Calendar } from "lucide-react";

interface CallDetailsCardProps {
  callId: string;
  agentId: string;
  customerName: string;
  startTimestamp: number;
  endTimestamp: number;
  durationMs: number;
  overallSentiment: string;
}

const CallDetailsCard = ({
  callId,
  agentId,
  customerName,
  startTimestamp,
  endTimestamp,
  durationMs,
  overallSentiment,
}: CallDetailsCardProps) => {
  const formatDate = (timestamp: number) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatDuration = (ms: number) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  const getSentimentColor = (sentiment: string) => {
    const lower = sentiment.toLowerCase();
    if (lower.includes("positive")) return "success";
    if (lower.includes("negative")) return "destructive";
    return "warning";
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Call Details</CardTitle>
          {/* <Badge variant={getSentimentColor(overallSentiment) as any}>
            {overallSentiment}
          </Badge> */}
          <Badge variant={getSentimentColor(overallSentiment) as any}>
            Call
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex items-center gap-3">
          <Phone className="h-4 w-4 text-muted-foreground" />
          <div>
            <p className="text-xs text-muted-foreground">Call ID</p>
            <p className="text-sm font-medium truncate">{callId}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <User className="h-4 w-4 text-muted-foreground" />
          <div>
            <p className="text-xs text-muted-foreground">Customer</p>
            <p className="text-sm font-medium">{customerName}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Clock className="h-4 w-4 text-muted-foreground" />
          <div>
            <p className="text-xs text-muted-foreground">Duration</p>
            <p className="text-sm font-medium">{formatDuration(durationMs)}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Calendar className="h-4 w-4 text-muted-foreground" />
          <div>
            <p className="text-xs text-muted-foreground">Start Timep</p>
            <p className="text-sm font-medium">{formatDate(startTimestamp)}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CallDetailsCard;
