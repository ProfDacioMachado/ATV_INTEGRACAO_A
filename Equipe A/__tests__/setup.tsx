import { jest } from "@jest/globals"
import "@testing-library/jest-dom"

jest.mock("recharts", () => {
  const React = require("react")
  return {
    ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
      <div className="recharts-wrapper">{children}</div>
    ),
    BarChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    Bar: () => <div />,
    XAxis: ({ dataKey }: { dataKey: string }) => <div>{dataKey}</div>,
    YAxis: () => <div />,
    CartesianGrid: () => <div />,
    Tooltip: () => <div />,
    LineChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    Line: () => <div />,
    Legend: () => <div />,
  }
})
