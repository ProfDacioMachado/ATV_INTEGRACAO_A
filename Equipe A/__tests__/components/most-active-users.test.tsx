import { render, screen } from "@testing-library/react"
import { MostActiveUsers } from "@/components/most-active-users"

describe("MostActiveUsers", () => {
  it("deve renderizar o título do card", () => {
    render(<MostActiveUsers />)

    expect(screen.getByText("Usuários Mais Ativos")).toBeInTheDocument()
    expect(screen.getByText("Ranking dos usuários com mais empréstimos")).toBeInTheDocument()
  })

  it("deve renderizar todos os usuários", () => {
    render(<MostActiveUsers />)

    expect(screen.getByText("Maria Silva")).toBeInTheDocument()
    expect(screen.getByText("João Santos")).toBeInTheDocument()
    expect(screen.getByText("Ana Costa")).toBeInTheDocument()
  })

  it("deve exibir badges de categoria corretas", () => {
    render(<MostActiveUsers />)

    expect(screen.getByText("Ouro")).toBeInTheDocument()
    expect(screen.getByText("Prata")).toBeInTheDocument()
    expect(screen.getByText("Bronze")).toBeInTheDocument()
  })

  it("deve exibir o número de empréstimos de cada usuário", () => {
    render(<MostActiveUsers />)

    expect(screen.getByText("87 empréstimos")).toBeInTheDocument()
    expect(screen.getByText("72 empréstimos")).toBeInTheDocument()
    expect(screen.getByText("65 empréstimos")).toBeInTheDocument()
  })
})
