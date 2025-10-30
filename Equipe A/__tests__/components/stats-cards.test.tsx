import { render, screen } from "@testing-library/react"
import { StatsCards } from "@/components/stats-cards"

describe("StatsCards", () => {
  it("deve renderizar todos os 4 cards de estatísticas", () => {
    render(<StatsCards />)

    expect(screen.getByText("Total de Empréstimos")).toBeInTheDocument()
    expect(screen.getByText("Usuários Ativos")).toBeInTheDocument()
    expect(screen.getByText("Livros em Circulação")).toBeInTheDocument()
    expect(screen.getByText("Tempo Médio de Empréstimo")).toBeInTheDocument()
  })

  it("deve exibir os valores corretos das estatísticas", () => {
    render(<StatsCards />)

    expect(screen.getByText("1,284")).toBeInTheDocument()
    expect(screen.getByText("342")).toBeInTheDocument()
    expect(screen.getByText("156")).toBeInTheDocument()
    expect(screen.getByText("14 dias")).toBeInTheDocument()
  })

  it("deve exibir as mudanças percentuais", () => {
    render(<StatsCards />)

    expect(screen.getByText("+12.5%")).toBeInTheDocument()
    expect(screen.getByText("+8.2%")).toBeInTheDocument()
    expect(screen.getByText("-3.1%")).toBeInTheDocument()
    expect(screen.getByText("+2 dias")).toBeInTheDocument()
  })

  it("deve aplicar cores corretas baseadas na tendência", () => {
    const { container } = render(<StatsCards />)

    const upTrends = container.querySelectorAll(".text-green-600")
    const downTrends = container.querySelectorAll(".text-red-600")

    expect(upTrends.length).toBe(2) // +12.5% e +8.2%
    expect(downTrends.length).toBe(1) // -3.1%
  })
})
