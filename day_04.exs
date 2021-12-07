defmodule Day_04 do


  def play() do
    load_puzzle()

  end

  defp is_winning_board?(board) do
    row_match = board
    |> Enum.any?(&Enum.all?(&1, fn x -> x == -1 end))

    col_match = board
    |> transpose
    |> Enum.any?(&Enum.all?(&1, fn x -> x == -1 end))

    row_match || col_match
  end

  # Transposes a list of lists [[a, b], [c, d]] -> [[a, c], [b, d]]
  defp transpose(list), do: list |> List.zip |> Enum.map(&Tuple.to_list/1)

  defp load_puzzle() do
    lines = File.read!("inputs/day_04.txt")
    |> String.replace("\r", "")
    |> String.split("\n")

    moves =
      lines
      |> Enum.at(0) |> String.split("")

    boards = lines
      |> Enum.slice(2, 999_999)
      |> Enum.chunk_by(&(&1 == ""))
      |> Enum.reject(&(&1 == [""]))
      |> Enum.map(&build_board/1)
    %{moves: moves, boards: boards}
    |> IO.inspect()
   end

   # Input: ["22 13 17 11  0", " 8  2 23  4 24", "21  9 14 16  7", " 6 10  3 18  5", " 1 12 20 15 19"]
   # Output: [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5],[1, 12, 20, 15, 19]]
   defp build_board(list_of_strings) do
     list_of_strings
     |> Enum.map(fn row ->
        row
        |> String.graphemes()
        |> Enum.chunk_every(3)
        |> Enum.map(fn cell -> Enum.join(cell, "") |> String.trim() |> String.to_integer() end)
     end)
   end
end

Day_04.play()
