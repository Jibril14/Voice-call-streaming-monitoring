import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { User, Headset } from "lucide-react";

interface TranscriptEntry {
  role: "agent" | "user";
  content: string;
  words: Array<{ word: string; start: number; end: number }>;
  "sentiment score": number;
}

interface TranscriptViewProps {
  transcriptObject: TranscriptEntry[];
}

const TranscriptView = ({ transcriptObject }: TranscriptViewProps) => {
  const getSentimentBadge = (score: number) => {
    if (score >= 0.7) return { variant: "success", label: "Positive" };
    if (score >= 0.4) return { variant: "warning", label: "Neutral" };
    return { variant: "destructive", label: "Negative" };
  };

  const getSentimentColor = (score: number) => {
    if (score >= 0.7) return "border-l-success";
    if (score >= 0.4) return "border-l-warning";
    return "border-l-destructive";
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle>Call Transcript</CardTitle>
        <CardDescription>
          Conversation transcript with sentiment indicators
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[400px] pr-4">
          <div className="space-y-4">
            {transcriptObject.map((entry, index) => {
              const sentiment = getSentimentBadge(entry["sentiment score"]);
              const colorClass = getSentimentColor(entry["sentiment score"]);
              
              return (
                <div
                  key={index}
                  className={`p-4 border-l-4 ${colorClass} bg-secondary/30 rounded-r-lg transition-all hover:bg-secondary/50`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {entry.role === "agent" ? (
                        <Headset className="h-4 w-4 text-primary" />
                      ) : (
                        <User className="h-4 w-4 text-chart-user" />
                      )}
                      <span className="font-semibold text-sm capitalize">
                        {entry.role}
                      </span>
                      {entry.words.length > 0 && (
                        <span className="text-xs text-muted-foreground">
                          {entry.words[0].start.toFixed(1)}s
                        </span>
                      )}
                    </div>
                    <Badge variant={sentiment.variant as any} className="text-xs">
                      {sentiment.label} {(entry["sentiment score"] * 100).toFixed(0)}%
                    </Badge>
                  </div>
                  <p className="text-sm text-foreground leading-relaxed">
                    {entry.content}
                  </p>
                </div>
              );
            })}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default TranscriptView;
