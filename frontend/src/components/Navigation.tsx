import { Activity } from "lucide-react";

const Navigation = () => {
  return (
    <nav className="bg-card border-b border-border">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-primary p-2 rounded-lg">
              <Activity className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">CallSense AI</h1>
              <p className="text-xs text-muted-foreground">Sentiment Analysis Dashboard</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">Live Analysis</span>
            <div className="h-2 w-2 rounded-full bg-success animate-pulse" />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
