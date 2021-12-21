defmodule Day_17 do
  def part_1() do
  end
end

defmodule Operator do
  defstruct [:version, :type, :value]

  def parse(version, type, <<data::bitstring>>) do
    {value, rest} = decode(data, <<>>)
    {%__MODULE__{
      version: version,
      type: type,
      value:  value
    }, rest}
  end

  defp decode(<<0x00::size(1), size::size(15), data::bitstring>>, acc) do
    <<op_data::size(size), rest>> = data
    {op_data, rest}
  end
end

defmodule Literal_Value do
  defstruct [:version, :value]

  def parse(version, <<data::bitstring>>) do
    {value, rest} = decode(data, <<>>)
    {%__MODULE__{
      version: version,
      value:  value
    }, rest}
  end

  defp decode(<<0x01::size(1), value::size(4), rest::bitstring>>, acc), do: decode(rest, <<acc::bitstring, value::size(4)>>)

  defp decode(<<0x00::size(1), value::size(4), _padding::size(3), rest::bitstring>>, acc) do
    bit_size = bit_size(<<acc::bitstring, value::size(4)>>)
    <<n::size(bit_size)>> = <<acc::bitstring, value::size(4)>>
    {n, rest}
  end
end

defmodule BITS do
  def decode(<<version::size(3), 0x04::size(3), rest::bitstring>>, acc) do
    {struct, rest} = Literal_Value.parse(version, rest)
    decode(rest, acc ++ [struct])
  end

  def decode(<<version::size(3), operator_type::size(3), rest::bitstring>>, acc) do
    {struct, rest} = Operator.parse(version, operator_type, rest)
    decode(rest, acc ++ [struct])
  end

  def decode(<<>>, acc), do: acc
end

"38006F45291200" |> Base.decode16!() |> BITS.decode([]) |> IO.inspect()
