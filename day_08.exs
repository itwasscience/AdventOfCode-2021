defmodule Day_08 do

  def part_1() do
    unique_lengths = [2, 3, 4, 7]
    load_segments()

  end



  def load_segments() do
    segments = File.read!("inputs/day_08.txt")
    |> String.replace("\r", "")
    |> String.split(["\n", " | "])
    |> Enum.chunk_every(2)
    |> Enum.map(fn x ->
      [segments, result] = x
      %{segments: String.split(segments, " "), result: String.split(result, " ")}
    end)
  end

end


Day_08.load_segments()
