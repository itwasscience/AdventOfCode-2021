defmodule Day_06 do

  @part_1_days 256

  def part_1() do
    load_fishes() |> run_days(@part_1_days) |> IO.inspect() |> Enum.reduce(0, fn {_age, count}, sum -> sum + count end) |> IO.inspect()
  end

  defp run_days(fishes, _days_remaining = 0), do: fishes

  defp run_days(fishes, days_remaining) do
    new_fishes = fishes |> age_fish |> spawn_fish()
    run_days(new_fishes, days_remaining - 1)
  end

  defp age_fish(fishes), do: Enum.map(fishes, fn {age, count} -> {age - 1, count} end) |> Map.new()

  defp spawn_fish(fishes) do
    fish_to_spawn = Map.get(fishes, -1, 0)

    Enum.map(fishes, fn {age, count} ->
        if age == -1 do
          {6, count}
        else
          {age, count}
        end
      end)
    |> Enum.reduce(%{}, fn {age, count}, acc ->
      Map.update(acc, age, count, &(&1 + count))
    end)
    |> Map.new()
    |> Map.put(8, fish_to_spawn)
  end

  defp load_fishes() do
    [1,1,1,1,1,5,1,1,1,5,1,1,3,1,5,1,4,1,5,1,2,5,1,1,1,1,3,1,4,5,1,1,2,1,1,1,2,4,3,2,1,1,2,1,5,4,4,1,4,1,1,1,4,1,3,1,1,1,2,1,1,1,1,1,1,1,5,4,4,2,4,5,2,1,5,3,1,3,3,1,1,5,4,1,1,3,5,1,1,1,4,4,2,4,1,1,4,1,1,2,1,1,1,2,1,5,2,5,1,1,1,4,1,2,1,1,1,2,2,1,3,1,4,4,1,1,3,1,4,1,1,1,2,5,5,1,4,1,4,4,1,4,1,2,4,1,1,4,1,3,4,4,1,1,5,3,1,1,5,1,3,4,2,1,3,1,3,1,1,1,1,1,1,1,1,1,4,5,1,1,1,1,3,1,1,5,1,1,4,1,1,3,1,1,5,2,1,4,4,1,4,1,2,1,1,1,1,2,1,4,1,1,2,5,1,4,4,1,1,1,4,1,1,1,5,3,1,4,1,4,1,1,3,5,3,5,5,5,1,5,1,1,1,1,1,1,1,1,2,3,3,3,3,4,2,1,1,4,5,3,1,1,5,5,1,1,2,1,4,1,3,5,1,1,1,5,2,2,1,4,2,1,1,4,1,3,1,1,1,3,1,5,1,5,1,1,4,1,2,1]
    |> Enum.frequencies()
  end
end

Day_06.part_1()
