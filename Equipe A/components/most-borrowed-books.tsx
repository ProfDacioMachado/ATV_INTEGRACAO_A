"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export function MostBorrowedBooks() {
  const [data, setData] = useState<{ titulo: string; emprestimos: number }[]>([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/livros")
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.error("Erro ao carregar livros:", err));
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Livros Mais Emprestados</CardTitle>
        <CardDescription>Top 6 livros com maior número de empréstimos</CardDescription>
      </CardHeader>
      <CardContent>
        {data.length === 0 ? (
          <p className="text-muted-foreground">Carregando dados...</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="titulo"
                angle={-45}
                textAnchor="end"
                height={100}
                className="text-xs"
                tick={{ fill: "hsl(var(--muted-foreground))" }}
              />
              <YAxis tick={{ fill: "hsl(var(--muted-foreground))" }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "0.5rem",
                }}
              />
              <Bar dataKey="emprestimos" fill="hsl(var(--chart-1))" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
