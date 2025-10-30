import { render, screen } from "@testing-library/react"
import { MostBorrowedBooks } from "@/components/most-borrowed-books"

describe("MostBorrowedBooks", () => {
  it("deve renderizar o título do card", () => {
    render(<MostBorrowedBooks />)

    expect(screen.getByText("Livros Mais Emprestados")).toBeInTheDocument()
    expect(screen.getByText("Top 6 livros com maior número de empréstimos")).toBeInTheDocument()
  })

  it("deve renderizar todos os 6 livros", () => {
    render(<MostBorrowedBooks />)

    expect(screen.getByText("Dom Casmurro")).toBeInTheDocument()
    expect(screen.getByText("O Cortiço")).toBeInTheDocument()
    expect(screen.getByText("1984")).toBeInTheDocument()
    expect(screen.getByText("A Revolução dos Bichos")).toBeInTheDocument()
    expect(screen.getByText("Memórias Póstumas")).toBeInTheDocument()
    expect(screen.getByText("Grande Sertão: Veredas")).toBeInTheDocument()
  })

  it("deve renderizar o gráfico de barras", () => {
    const { container } = render(<MostBorrowedBooks />)

    const chart = container.querySelector(".recharts-wrapper")
    expect(chart).toBeInTheDocument()
  })
})
