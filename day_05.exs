defmodule Day_05 do
  def run() do
    vh_intersections = get_coord_pairs()
    |> build_vh_map()
    |> render_map()
    |> Enum.reduce(0, fn {_k, v}, acc -> if v > 1, do: acc + 1, else: acc end)
    IO.puts("Part 1: #{vh_intersections}")

    diag_intersections =  get_coord_pairs()
    |> build_diag_map()
    |> Enum.reduce(0, fn {_k, v}, acc -> if v > 1, do: acc + 1, else: acc end)
    IO.puts("Part 2: #{diag_intersections}")
  end

  def build_vh_map(lines) do
    Enum.reduce(lines, %{}, fn line, acc ->
      [x1, y1, x2, y2] = line
      # Vertical Lines Only
      coords = cond do
        x1 == x2 ->
          for x <- x1..x2, do: for(y <- y1..y2, do: [x, y])

        y1 == y2 ->
          for x <- x1..x2, do: for(y <- y1..y2, do: [x, y])

        true ->
          []
      end
      |> List.flatten()
      |> Enum.chunk_every(2)

      if Kernel.length(coords) > 0 do
        Enum.reduce(coords, acc, fn point, p_acc -> Map.put(p_acc, point, Map.get(acc, point, 0) + 1) end)
      else
        acc
      end
    end)
  end

  def build_diag_map(lines) do
    Enum.reduce(lines, %{}, fn line, acc ->
      [x1, y1, x2, y2] = line
      coords = cond do
        x1 == x2 ->
          for x <- x1..x2, do: for(y <- y1..y2, do: [x, y])

        y1 == y2 ->
          for x <- x1..x2, do: for(y <- y1..y2, do: [x, y])

        # Linear Interpolation
        true ->
            for x <- x1..x2 do
              for _y <- y1..y2 do
               iy = (y1 * (x2 - x) + y2 * (x - x1)) / (x2 - x1)
               [x, trunc(iy)]
              end
            end
      end
      |> List.flatten()
      |> Enum.chunk_every(2)

      if Kernel.length(coords) > 0 do
        Enum.reduce(coords, acc, fn point, p_acc -> Map.put(p_acc, point, Map.get(acc, point, 0) + 1) end)
      else
        acc
      end
    end)
  end

  def render_map(map_data) do
    for y <- 0..9 do
      for x <- 0..9 do
        IO.write("#{Map.get(map_data, [x,y], '.')}")
      end
      IO.write("\n")
    end
    map_data
  end

  def get_coord_pairs() do
    File.read!("inputs/day_05.txt")
    |> String.replace("\r", "")
    |> String.split("\n")
    |> Enum.map(&String.split(&1, [" -> ", ","]))
    |> Enum.map(fn x -> Enum.map(x, &String.to_integer(&1)) end)
  end
end

Day_05.run()
