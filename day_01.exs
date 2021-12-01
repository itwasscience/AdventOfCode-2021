defmodule Day_01 do
  def part_1() do
    get_depths()
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.map(fn [previous, current] -> current > previous end)
    |> Enum.count(& &1)
    |> IO.inspect()
  end

  def part_2() do
    get_depths()
    |> Enum.chunk_every(3, 1, :discard)
    |> Enum.map(&Enum.sum/1)
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.map(fn [previous, current] -> current > previous end)
    |> Enum.count(& &1)
    |> IO.inspect()
  end

  defp get_depths() do
    {:ok, input} = File.read("inputs/day_01.txt")

    input
    |> String.replace("\r", "")
    |> String.split("\n")
    |> Enum.map(fn x -> String.to_integer(x) end)
  end
end

Day_01.part_1()
Day_01.part_2()
