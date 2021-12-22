defmodule Operator do
  defstruct [:version, :type, :sub_packets]

  def parse(version, type, <<data::bitstring>>) do
    {sub_packets, rest} = decode(data)

    operator = %__MODULE__{
      version: version,
      type: type,
      sub_packets: sub_packets
    }

    {operator, rest}
  end

  defp decode(<<0x00::size(1), length::size(15), data::bitstring>>) do
    <<op_data::bits-size(length), rest::bitstring>> = data
    {sub_packets, _rest} = BITS.decode(op_data, [])
    {sub_packets, rest}
  end

  defp decode(<<0x01::size(1), sub_packet_count::size(11), data::bitstring>>) do
    BITS.decode(data, [], sub_packet_count)
  end
end

defmodule LiteralValue do
  defstruct [:version, :value]

  def parse(version, <<data::bitstring>>) do
    {value, rest} = decode(data, <<>>)

    {%__MODULE__{
       version: version,
       value: value
     }, rest}
  end

  defp decode(<<0x01::size(1), value::size(4), rest::bitstring>>, acc),
    do: decode(rest, <<acc::bitstring, value::size(4)>>)

  defp decode(<<0x00::size(1), value::size(4), rest::bitstring>>, acc) do
    bit_size = bit_size(<<acc::bitstring, value::size(4)>>)
    <<n::size(bit_size)>> = <<acc::bitstring, value::size(4)>>
    {n, rest}
  end
end

defmodule BITS do
  def decode(bitstring, acc, max_len \\ 999_999)
  def decode(<<0::size(1)>>, acc, _max_len), do: {acc, <<>>}
  def decode(<<0::size(2)>>, acc, _max_len), do: {acc, <<>>}
  def decode(<<0::size(3)>>, acc, _max_len), do: {acc, <<>>}
  def decode(<<0::size(4)>>, acc, _max_len), do: {acc, <<>>}
  def decode(<<0::size(5)>>, acc, _max_len), do: {acc, <<>>}
  def decode(<<0::size(6)>>, acc, _max_len), do: {acc, <<>>}
  def decode(<<0::size(7)>>, acc, _max_len), do: {acc, <<>>}
  def decode(<<>>, acc, _max_len), do: {acc, <<>>}

  def decode(<<version::size(3), 0x04::size(3), rest::bitstring>>, acc, max_len) do
    {struct, rest} = LiteralValue.parse(version, rest)
    new_acc = acc ++ [struct]

    if Kernel.length(new_acc) >= max_len,
      do: {new_acc, rest},
      else: decode(rest, acc ++ [struct], max_len)
  end

  def decode(<<version::size(3), operator_type::size(3), rest::bitstring>>, acc, max_len) do
    {struct, rest} = Operator.parse(version, operator_type, rest)
    new_acc = acc ++ [struct]

    if Kernel.length(new_acc) >= max_len,
      do: {new_acc, rest},
      else: decode(rest, acc ++ [struct], max_len)
  end
end

defmodule Day_17 do
  def part_1() do
    {result, _} = load_file() |> BITS.decode([])

    result
    |> Enum.reduce(0, fn x, acc -> acc + sum_versions(x) end)
    |> IO.inspect(limit: :infinity)
  end

  defp sum_versions(struct, acc \\ 0)

  defp sum_versions(struct = %Operator{}, acc),
    do:
      Enum.reduce(struct.sub_packets, acc + struct.version, fn x, x_acc ->
        x_acc + sum_versions(x)
      end)

  defp sum_versions(struct = %LiteralValue{}, acc), do: acc + struct.version

  def part_2() do
    {result, _} = load_file() |> BITS.decode([])
    result |> Enum.at(0) |> calc_values() |> Map.get(:value) |> IO.inspect(limit: :infinity)
  end

  defp calc_values(struct)

  defp calc_values(struct = %Operator{type: 0}),
    do:
      Map.put(
        struct,
        :value,
        Enum.reduce(struct.sub_packets, 0, fn x, acc -> acc + calc_values(x).value end)
      )

  defp calc_values(struct = %Operator{type: 1}),
    do:
      Map.put(
        struct,
        :value,
        Enum.reduce(struct.sub_packets, 1, fn x, acc -> acc * calc_values(x).value end)
      )

  defp calc_values(struct = %Operator{type: 2}),
    do:
      Map.put(
        struct,
        :value,
        Enum.map(struct.sub_packets, fn x -> calc_values(x).value end) |> Enum.min()
      )

  defp calc_values(struct = %Operator{type: 3}),
    do:
      Map.put(
        struct,
        :value,
        Enum.map(struct.sub_packets, fn x -> calc_values(x).value end) |> Enum.max()
      )

  defp calc_values(struct = %Operator{type: 5}) do
    if struct.sub_packets |> Enum.at(0) |> calc_values() |> Map.get(:value) >
         struct.sub_packets |> Enum.at(1) |> calc_values() |> Map.get(:value) do
      Map.put(struct, :value, 1)
    else
      Map.put(struct, :value, 0)
    end
  end

  defp calc_values(struct = %Operator{type: 6}) do
    if struct.sub_packets |> Enum.at(0) |> calc_values() |> Map.get(:value) <
         struct.sub_packets |> Enum.at(1) |> calc_values() |> Map.get(:value) do
      Map.put(struct, :value, 1)
    else
      Map.put(struct, :value, 0)
    end
  end

  defp calc_values(struct = %Operator{type: 7}) do
    if struct.sub_packets |> Enum.at(0) |> calc_values() |> Map.get(:value) ==
         struct.sub_packets |> Enum.at(1) |> calc_values() |> Map.get(:value) do
      Map.put(struct, :value, 1)
    else
      Map.put(struct, :value, 0)
    end
  end

  defp calc_values(struct = %LiteralValue{}), do: struct

  def load_file(), do: File.read!("inputs/day_16.txt") |> Base.decode16!()
end

Day_17.part_1()
Day_17.part_2()
