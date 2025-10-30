import { render, screen } from "@testing-library/react"
import { ReportsHeader } from "@/components/reports-header"

describe("ReportsHeader", () => {
  it("deve renderizar o título principal", () => {
    render(<ReportsHeader />)

    expect(screen.getByText("Relatórios da Biblioteca")).toBeInTheDocument()
  })

  it("deve renderizar a descrição", () => {
    render(<ReportsHeader />)

    expect(screen.getByText(/Análise completa de empréstimos/i)).toBeInTheDocument()
  })

  it("deve renderizar o botão de exportar", () => {
    render(<ReportsHeader />)

    const exportButton = screen.getByRole("button", { name: /exportar/i })
    expect(exportButton).toBeInTheDocument()
  })
})
