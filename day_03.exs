defmodule Day_03 do

  def part_1() do
    bit_freqs = get_binaries() |> get_bit_frequencies()

    gamma_rate = bit_freqs |> calc_gamma_rate
    epsilon_rate = bit_freqs |> calc_epsilon_rate

    IO.puts("Part 1: #{gamma_rate * epsilon_rate}")
  end

  defp calc_gamma_rate(list) do
    list
    |> Enum.map(fn x -> x |> Enum.max_by(fn {_k, v} -> v end) end)
    |> string_list_to_int()
  end

  defp calc_epsilon_rate(list) do
    list
    |> Enum.map(fn x -> x |> Enum.min_by(fn {_k, v} -> v end) end)
    |> string_list_to_int()
  end

  defp string_list_to_int(list) do
    list
    |> Enum.map(fn x -> x |> Tuple.to_list |> Enum.at(0) end)
    |> Enum.join("")
    |> String.to_integer(2)
  end

  defp get_bit_frequencies(list), do: list |> transpose() |> Enum.map(&Enum.frequencies/1)

  # Transposes a list of lists [[a, b], [c, d]] -> [[a, c], [b, d]]
  defp transpose(list), do: list |> List.zip |> Enum.map(&Tuple.to_list/1)

  def get_binaries() do
    File.read!("inputs/day_03.txt")
    |> String.replace("\r", "")
    |> String.split("\n")
    |> Enum.map(fn x -> String.graphemes(x) end)
  end
end

Day_03.part_1()
