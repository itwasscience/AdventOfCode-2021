defmodule Day_14 do
  # Part 1 - Naieve, surely we can just use lists and count the resulting polymer's atoms
  def part_1() do
    %{polymer: polymer, rules: rules} = load_polymer_data()

    {{_min_element, min_count}, {_max_element, max_count}} = polymer
    |> build_polymer(rules, 10)
    |> Enum.frequencies()
    |> Enum.min_max_by(fn {_k, v} -> v end)

    IO.puts("Part 1: #{max_count - min_count}")
  end

  defp build_polymer(polymer, _rules, 0), do: polymer

  defp build_polymer(polymer, rules, cycles_left) do
    polymer
    |> Enum.intersperse("")
    |> Enum.chunk_every(3, 2)
    |> Enum.map(&inject_polymer(&1, rules))
    |> List.flatten()
    |> build_polymer(rules, cycles_left - 1)
  end

  defp inject_polymer([first, _, last], rules), do: [first, Map.fetch!(rules, "#{first}#{last}")]

  defp inject_polymer(list, _rules), do: list

  # Part 2 - We don't need to know the actual atmoic structure, just the counts
  def part_2() do
    %{polymer: polymer, rules: rules} = load_polymer_data()

    polymer_pair_counts = polymer
    |> Enum.chunk_every(2, 1)
    |> Enum.filter(fn x -> Kernel.length(x) == 2 end)
    |> Enum.reduce(%{}, fn x, acc ->
      pair = Enum.join(x, "")
      Map.put(acc, pair, Map.get(acc, pair, 0) + 1)
    end)

    empty_pair_counts = rules
    |> Enum.reduce(%{}, fn {k, _v}, acc -> Map.put(acc, k, 0) end)

    starting_pair_counts = empty_pair_counts |> Map.merge(polymer_pair_counts)
    counting_rules = generate_counting_rules(rules)

    starting_pair_counts
    |> run_cycle(counting_rules, empty_pair_counts, 1)
    |> IO.inspect()
    |> count_elements()
    |> IO.inspect()
  end

  defp count_elements(pair_counts) do
    Enum.reduce(pair_counts, %{}, fn {k, v}, acc ->
      [element_one, element_two] = String.graphemes(k)
      IO.puts("Adding #{v} to #{element_one}, #{element_two}")
      acc
      |> Map.put(element_one, v + Map.get(acc, element_one, 0))
      |> Map.put(element_two, v + Map.get(acc, element_two, 0))
    end)
  end

  defp run_cycle(pair_counts, _counting_rules, _empty_pair_counts, 0), do: pair_counts

  defp run_cycle(pair_counts, counting_rules, empty_pair_counts, cycles_left) do
    pair_counts
    |> Enum.reduce(empty_pair_counts, fn {k, v}, acc ->
      [first_key, second_key] = counting_rules[k]
      #IO.puts("Adding #{v} to #{first_key}, #{second_key}")
      acc
      |> Map.put(first_key, v + Map.get(acc, first_key))
      |> Map.put(second_key, v + Map.get(acc, second_key))
    end)
    # Subtract out the original pairings so we don't double count
    |> Enum.reduce(%{}, fn {k, v}, acc ->
      new_val = v - Map.get(pair_counts, k)
      if new_val >= 0, do: Map.put(acc, k, new_val), else: Map.put(acc, k, 0)
    end)
    |> run_cycle(counting_rules, empty_pair_counts, cycles_left - 1)
  end

  defp generate_counting_rules(rules) do
    rules
    |> Enum.reduce(%{}, fn {k, v}, acc ->
      [first, second] = String.graphemes(k)
      Map.put(acc, k, [first <> v, v <> second])
    end)
  end

  def load_polymer_data() do
    {raw_polymer, raw_rules} = File.read!("inputs/day_14.txt")
    |> String.replace("\r", "")
    |> String.split("\n")
    |> Enum.split(2)

    rules = raw_rules
    |> Enum.reduce(%{}, fn r, acc ->
      [pair, insertion]= String.split(r, " -> ")
      Map.put(acc, pair, insertion)
    end)

    %{polymer: Enum.at(raw_polymer, 0) |> String.graphemes(), rules: rules}
  end
end

Day_14.part_2()
