import { NavLink } from "react-router-dom";
import { Home, Activity, FileText } from "lucide-react";
import { cn } from "@/lib/utils";

export const Navigation = () => {
  const links = [
    { to: "/", icon: Home, label: "Dashboard" },
    { to: "/status", icon: Activity, label: "Status" },
    { to: "/logs", icon: FileText, label: "Logs" },
  ];

  return (
    <nav className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <div className="flex gap-1">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                end
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors border-b-2",
                    isActive
                      ? "border-primary text-primary"
                      : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
                  )
                }
              >
                <Icon className="w-4 h-4" />
                {link.label}
              </NavLink>
            );
          })}
        </div>
      </div>
    </nav>
  );
};
