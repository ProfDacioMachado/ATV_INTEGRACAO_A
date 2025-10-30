import { FileText, Calendar } from "lucide-react"
import { Button } from "@/components/ui/button"

export function ReportsHeader() {
  return (
    <header className="border-b border-border bg-card">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <FileText className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-balance">Relatórios da Biblioteca</h1>
              <p className="text-sm text-muted-foreground">Equipe 4 - Sistema de Gestão</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button variant="outline" size="sm">
              <Calendar className="mr-2 h-4 w-4" />
              Últimos 30 dias
            </Button>
            <Button size="sm">Exportar Relatório</Button>
          </div>
        </div>
      </div>
    </header>
  )
}
