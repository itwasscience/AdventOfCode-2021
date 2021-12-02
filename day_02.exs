defmodule Day_02 do
  defstruct depth: 0, h_pos: 0, aim: 0

  def part_1() do
    final_coords =
      get_directions()
      |> Enum.reduce(%__MODULE__{}, fn step, acc -> navigate_simple(step, acc) end)

    IO.puts("Part 1: #{final_coords.depth * final_coords.h_pos}")
  end

  def part_2() do
    final_coords =
      get_directions()
      |> Enum.reduce(%__MODULE__{}, fn step, acc -> navigate_with_aim(step, acc) end)

    IO.puts("Part 2: #{final_coords.depth * final_coords.h_pos}")
  end

  defp navigate_simple(%{direction: "forward", value: value}, cur_pos = %{h_pos: h_pos}),
    do: %{cur_pos | h_pos: h_pos + value}

  defp navigate_simple(%{direction: "down", value: value}, cur_pos = %{depth: depth}),
    do: %{cur_pos | depth: depth + value}

  defp navigate_simple(%{direction: "up", value: value}, cur_pos = %{depth: depth}),
    do: %{cur_pos | depth: depth - value}

  defp navigate_simple(_, cur_pos), do: cur_pos

  defp navigate_with_aim(%{direction: "forward", value: value}, %__MODULE__{
         depth: depth,
         h_pos: h_pos,
         aim: aim
       }),
       do: %__MODULE__{depth: depth + value * aim, h_pos: h_pos + value, aim: aim}

  defp navigate_with_aim(%{direction: "down", value: value}, %__MODULE__{
         depth: depth,
         h_pos: h_pos,
         aim: aim
       }),
       do: %__MODULE__{depth: depth, h_pos: h_pos, aim: aim + value}

  defp navigate_with_aim(%{direction: "up", value: value}, %__MODULE__{
         depth: depth,
         h_pos: h_pos,
         aim: aim
       }),
       do: %__MODULE__{depth: depth, h_pos: h_pos, aim: aim - value}

  defp navigate_with_aim(_, cur_pos), do: cur_pos

  defp get_directions() do
    File.read!("inputs/day_02.txt")
    |> String.replace("\r", "")
    |> String.split("\n")
    |> Enum.map(fn x ->
      [direction, value] = String.split(x, " ")
      %{:direction => direction, :value => String.to_integer(value)}
    end)
  end
end

Day_02.part_1()
Day_02.part_2()
