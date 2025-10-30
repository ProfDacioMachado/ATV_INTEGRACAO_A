import { BookOpen, Users, TrendingUp, Clock } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

const stats = [
  {
    title: "Total de Empréstimos",
    value: "1,284",
    change: "+12.5%",
    icon: BookOpen,
    trend: "up",
  },
  {
    title: "Usuários Ativos",
    value: "342",
    change: "+8.2%",
    icon: Users,
    trend: "up",
  },
  {
    title: "Livros em Circulação",
    value: "156",
    change: "-3.1%",
    icon: TrendingUp,
    trend: "down",
  },
  {
    title: "Tempo Médio de Empréstimo",
    value: "14 dias",
    change: "+2 dias",
    icon: Clock,
    trend: "neutral",
  },
]

export function StatsCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => {
        const Icon = stat.icon
        return (
          <Card key={stat.title}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Icon className="h-6 w-6" />
                </div>
                <span
                  className={`text-sm font-medium ${
                    stat.trend === "up"
                      ? "text-green-600"
                      : stat.trend === "down"
                        ? "text-red-600"
                        : "text-muted-foreground"
                  }`}
                >
                  {stat.change}
                </span>
              </div>
              <div className="mt-4">
                <p className="text-sm text-muted-foreground">{stat.title}</p>
                <p className="mt-1 text-2xl font-bold">{stat.value}</p>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
