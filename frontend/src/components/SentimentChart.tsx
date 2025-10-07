import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

interface TranscriptEntry {
  role: "agent" | "user";
  content: string;
  words: Array<{ word: string; start: number; end: number }>;
  "sentiment score": number;
}

interface SentimentChartProps {
  transcriptObject: TranscriptEntry[];
}

const SentimentChart = ({ transcriptObject }: SentimentChartProps) => {
  // Transform transcript data into chart data
  const chartData = transcriptObject.map((entry, index) => {
    // Use the start time of the first word as the timestamp
    const timestamp = entry.words.length > 0 ? entry.words[0].start : index;
    
    return {
      time: timestamp.toFixed(1),
      agent: entry.role === "agent" ? entry["sentiment score"] : null,
      user: entry.role === "user" ? entry["sentiment score"] : null,
    };
  });

  // Fill in gaps - if agent spoke, find closest user sentiment and vice versa
  const filledData = chartData.map((point, index) => {
    const result = { ...point };
    
    if (point.agent === null) {
      // Find the most recent agent sentiment
      for (let i = index - 1; i >= 0; i--) {
        if (chartData[i].agent !== null) {
          result.agent = chartData[i].agent;
          break;
        }
      }
    }
    
    if (point.user === null) {
      // Find the most recent user sentiment
      for (let i = index - 1; i >= 0; i--) {
        if (chartData[i].user !== null) {
          result.user = chartData[i].user;
          break;
        }
      }
    }
    
    return result;
  });

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle>Sentiment Timeline</CardTitle>
        <CardDescription>
          Real-time sentiment analysis throughout the conversation
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={filledData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis 
              dataKey="time" 
              label={{ value: "Time (seconds)", position: "insideBottom", offset: -5 }}
              className="text-xs"
            />
            <YAxis 
              domain={[0, 1]} 
              label={{ value: "Sentiment Score", angle: -90, position: "insideLeft" }}
              className="text-xs"
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: "hsl(var(--card))", 
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)"
              }}
              formatter={(value: any) => (value !== null ? value.toFixed(2) : "N/A")}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="agent" 
              stroke="hsl(var(--chart-agent))" 
              strokeWidth={2.5}
              name="Agent"
              dot={{ fill: "hsl(var(--chart-agent))", r: 4 }}
              activeDot={{ r: 6 }}
              connectNulls
            />
            <Line 
              type="monotone" 
              dataKey="user" 
              stroke="hsl(var(--chart-user))" 
              strokeWidth={2.5}
              name="User"
              dot={{ fill: "hsl(var(--chart-user))", r: 4 }}
              activeDot={{ r: 6 }}
              connectNulls
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default SentimentChart;
