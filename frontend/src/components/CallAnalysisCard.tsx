import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText } from "lucide-react";

interface CallAnalysisCardProps {
  callSummary: string;
}

const CallAnalysisCard = ({ callSummary }: CallAnalysisCardProps) => {
  return (
    <Card className="shadow-lg">
      <CardHeader>
        <div className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-primary" />
          <CardTitle>Call Summary</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-foreground leading-relaxed">
          {callSummary}
        </p>
      </CardContent>
    </Card>
  );
};

export default CallAnalysisCard;
