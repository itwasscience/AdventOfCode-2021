defmodule Day_17 do
  def part_1() do
  end
end

defmodule BITS_Literal do
  defstruct [:version, :value]

  def parse(<<version::size(3), data::bitstring>>) do

  end
end

defmodule BITS do
  # def decode(<<version::size(3), rest::bitstring>>), do: version |> IO.inspect()

  def decode(
        <<version::size(3), 0x04::size(3), 0x01::size(1), a::size(4), 0x01::size(1), b::size(4),
          0x00::size(1), c::size(4), _padding::bitstring>>
      ) do
    <<value::size(12)>> = <<(<<a::4>>)::bitstring, <<b::4>>::bitstring, <<c::4>>::bitstring>>
    %BITS_Literal{version: version, value: value}
  end

  def decode_literal(<<0x01::size(1), value::size(4), rest::bitstring>>, acc), do
    decode_literal <<>>
  end

  def decode_literal(<<0x00::size(1), value::size(4), rest::bitstring>>, acc), do {acc, rest}

end

BITS.decode("D2FE28" |> Base.decode16!()) |> IO.inspect()
