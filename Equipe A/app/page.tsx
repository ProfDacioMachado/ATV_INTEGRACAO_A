import { ReportsHeader } from "@/components/reports-header"
import { StatsCards } from "@/components/stats-cards"
import { MostBorrowedBooks } from "@/components/most-borrowed-books"
import { MostActiveUsers } from "@/components/most-active-users"
import { BorrowingTrends } from "@/components/borrowing-trends"

export default function ReportsPage() {
  return (
    <div className="min-h-screen bg-background">
      <ReportsHeader />

      <main className="container mx-auto px-4 py-8 space-y-8">
        <StatsCards />

        <div className="grid gap-8 lg:grid-cols-2">
          <MostBorrowedBooks />
          <MostActiveUsers />
        </div>

        <BorrowingTrends />
      </main>
    </div>
  )
}
