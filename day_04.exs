defmodule FinishedBoard do
  defstruct board: [], last_number: -1, score: 0, num_moves: 0
end

defmodule Day_04 do
  def play() do
    %{moves: moves, boards: boards} = load_puzzle()

    finished_boards =
      Enum.map(boards, fn board ->
        Enum.reduce_while(moves, %{board: board, num_moves: 0}, fn move, acc ->
          new_board = play_move(acc.board, move)
          num_moves = acc.num_moves + 1

          if is_winning_board?(new_board) do
            {:halt,
             %FinishedBoard{
               last_number: move,
               board: new_board,
               score: calc_score(new_board),
               num_moves: num_moves
             }}
          else
            {:cont, %{board: new_board, num_moves: num_moves}}
          end
        end)
      end)
      |> Enum.sort_by(fn x -> x.num_moves end)

    best_board = Enum.at(finished_boards, 0)
    worst_board = Enum.at(finished_boards, -1)
    IO.puts("Part 1: #{best_board.score * best_board.last_number}")
    IO.puts("Part 2: #{worst_board.score * worst_board.last_number}")
  end

  defp play_move(board, move), do: Enum.map(board, fn x -> if x == move, do: -1, else: x end)

  defp is_winning_board?(board) do
    board_2d = board |> Enum.chunk_every(5)
    row_match = board_2d |> Enum.any?(&Enum.all?(&1, fn x -> x == -1 end))
    col_match = board_2d |> transpose |> Enum.any?(&Enum.all?(&1, fn x -> x == -1 end))

    row_match || col_match
  end

  defp calc_score(board), do: board |> Enum.reject(fn x -> x < 0 end) |> Enum.sum()

  # Transposes a list of lists [[a, b], [c, d]] -> [[a, c], [b, d]]
  defp transpose(list), do: list |> List.zip() |> Enum.map(&Tuple.to_list/1)

  defp load_puzzle() do
    lines =
      File.read!("inputs/day_04.txt")
      |> String.replace("\r", "")
      |> String.split("\n")

    moves = lines |> Enum.at(0) |> String.split(",") |> Enum.map(&String.to_integer(&1))

    boards =
      lines
      |> Enum.slice(2, 999_999)
      |> Enum.chunk_by(&(&1 == ""))
      |> Enum.reject(&(&1 == [""]))
      |> Enum.map(&build_board/1)

    %{moves: moves, boards: boards}
  end

  # Input: ["22 13 17 11  0", " 8  2 23  4 24", "21  9 14 16  7", " 6 10  3 18  5", " 1 12 20 15 19"]
  # Output: [22, 13, 17, 11, 0, 8, 2, 23, 4, 24, 21, 9, 14, 16, 7, 6, 10, 3, 18, 5, 1, 12, 20, 15, 19]
  defp build_board(list_of_strings) do
    list_of_strings
    |> Enum.map(fn row ->
      row
      |> String.graphemes()
      |> Enum.chunk_every(3)
      |> Enum.map(fn cell -> Enum.join(cell, "") |> String.trim() |> String.to_integer() end)
    end)
    |> List.flatten()
  end
end

Day_04.play()
