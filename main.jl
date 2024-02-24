using Pkg;
Pkg.activate(@__DIR__);
Pkg.instantiate();

using DataFrames, CSV, CairoMakie;

using Dates;

df = DataFrame(CSV.File("./data/1st_quater_2023_BTC.csv"))

tn = 1:89;
t_full = range(start = Dates.Date(2023, 1, 1), step = Dates.Day(1), length = 89)
close_price = df.Close;
class = df.class;


# transform decisions vector into vector of profits

profit = zeros(length(class))

prev_buy_ind = 0;

for i in eachindex(class)
    class[i] == 1 ? prev_buy_ind = i : nothing
    class[i] == 0 ? profit[i] = close_price[i] - close_price[prev_buy_ind] : nothing
end;

total_profit = sum(profit) # 8378.50390625

profit_norm = profit ./ maximum(profit);

# get usdt data

using YFinance;

usdt_data =
    get_prices("USDT-USD", interval = "1d", startdt = t_full[1], enddt = t_full[end]);

usdt_vol = usdt_data["vol"];

usdt_vol_norm = usdt_vol ./ maximum(usdt_vol)

# prepare plot

t_strings = string.(t_full);

fig = Figure();

ax1 = Axis(
    fig[1, 1],
    title = "Прибыль по разметке бота (нормировка)",
    xlabel = "дата",
    ylabel = "прибыль [произв.ед.]",
    xticks = (tn[1:5:end], t_strings[1:5:end]),
    xticklabelrotation = pi / 4,
    xminorticks = IntervalsBetween(5),
    xminorticksvisible = true,
    xminorgridvisible = true,
    yticks = -0.2:0.2:1,
    yminorticks = IntervalsBetween(2),
    yminorticksvisible = true,
    yminorgridvisible = true,
);
ax2 = Axis(
    fig[2, 1],
    title = "Объем торгов USDT (данные YF, нормировка)",
    xlabel = "дата",
    ylabel = "объем [произв.ед.]",
    xticks = (tn[1:5:end], t_strings[1:5:end]),
    xticklabelrotation = pi / 4,
    xminorticks = IntervalsBetween(5),
    xminorticksvisible = true,
    xminorgridvisible = true,
    yticks = 0:0.2:1,
    yminorticks = IntervalsBetween(2),
    yminorticksvisible = true,
    yminorgridvisible = true,
);


lines!(ax1, tn, profit_norm, color = :red);
lines!(ax2, tn, usdt_vol_norm, color = :darkblue);

limits!(ax1, tn[1], tn[end], -0.2, 1)
limits!(ax2, tn[1], tn[end], 0, 1)

fig

save("./plots/usdt_vol.png", fig, px_per_unit = 3)


# save usdt trading volume data

using DelimitedFiles

writedlm("./data/usdt_volume.csv", usdt_vol_norm);
