import { render, screen } from "@testing-library/react"
import ReportsPage from "@/app/page"

describe("ReportsPage", () => {
  it("deve renderizar o header", () => {
    render(<ReportsPage />)

    expect(screen.getByText("Relatórios da Biblioteca")).toBeInTheDocument()
  })

  it("deve renderizar todos os componentes principais", () => {
    render(<ReportsPage />)

    // Verifica se os cards de estatísticas estão presentes
    expect(screen.getByText("Total de Empréstimos")).toBeInTheDocument()

    // Verifica se o componente de livros mais emprestados está presente
    expect(screen.getByText("Livros Mais Emprestados")).toBeInTheDocument()

    // Verifica se o componente de usuários mais ativos está presente
    expect(screen.getByText("Usuários Mais Ativos")).toBeInTheDocument()

    // Verifica se o componente de tendências está presente
    expect(screen.getByText("Tendências de Empréstimos")).toBeInTheDocument()
  })

  it("deve ter a estrutura de layout correta", () => {
    const { container } = render(<ReportsPage />)

    const main = container.querySelector("main")
    expect(main).toHaveClass("container", "mx-auto")
  })
})
