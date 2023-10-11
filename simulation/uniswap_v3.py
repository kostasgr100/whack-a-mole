import math
import numpy as np

class TickMap:
    def __init__(self):
        self.ticks = {}

    def add_liquidity(self, tick, liquidity):
        self.ticks[tick] = self.ticks.get(tick, 0) + liquidity

    def remove_liquidity(self, tick, liquidity):
        if tick in self.ticks:
            self.ticks[tick] -= liquidity
            if self.ticks[tick] <= 0:
                del self.ticks[tick]

class UniswapV3Simulator:
    def __init__(self):
        self.tick_map = TickMap()

    def sqrtx96_to_tick(self, sqrtx96: float):
        return math.floor(math.log(sqrtx96 * 2 ** (-96), math.sqrt(1.0001)))

    def tick_to_sqrt(self, tick: float):
        return math.sqrt(1.0001) ** tick

    def get_amount_out_multi_tick(self, amount_in, start_tick, end_tick, tick_spacing):
        amount_out = 0
        remaining_amount_in = amount_in
        current_tick = start_tick

        while current_tick <= end_tick and remaining_amount_in > 0:
            sqrt_start = self.tick_to_sqrt(current_tick)
            sqrt_end = self.tick_to_sqrt(current_tick + tick_spacing)
            liquidity = self.tick_map.ticks.get(current_tick, 0)

            if liquidity > 0:
                x_start = sqrt_start ** 2 / (2 ** 96)
                x_end = sqrt_end ** 2 / (2 ** 96)

                L = min(
                    (x_end * liquidity) / ((x_end - x_start) ** 0.5),
                    (x_start * liquidity) / ((x_end - x_start) ** 0.5)
                )

                delta_y = (remaining_amount_in * x_end) / x_start

                if delta_y > L:
                    delta_y = L

                amount_out += delta_y
                remaining_amount_in -= (delta_y * x_start) / x_end

            current_tick += tick_spacing

        if remaining_amount_in > 0:
            print("Warning: Order not fully filled. Remaining amount:", remaining_amount_in)
        
        return amount_out

    # (Rest of the methods can remain unchanged)

if __name__ == '__main__':
    simulator = UniswapV3Simulator()
    simulator.tick_map.add_liquidity(5000, 100)
    simulator.tick_map.add_liquidity(6000, 200)

    amount_out = simulator.get_amount_out_multi_tick(10, 5000, 6000, 10)
    print("Amount out:", amount_out)
