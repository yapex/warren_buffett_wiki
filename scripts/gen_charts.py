"""生成巴菲特业绩图表：伯克希尔 + 合伙基金"""
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams['font.family'] = ['Heiti TC', 'PingFang SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUT = os.path.join(os.path.dirname(__file__), '..', 'wiki', 'assets')
os.makedirs(OUT, exist_ok=True)

# ================================================================
# 图1: 伯克希尔哈撒韦 vs 标普500 (1965–2024)
# ================================================================
years_brk = list(range(1965, 2025))
brk_pct = [49.5, -3.4, 13.3, 77.8, 19.4, -4.6, 80.5, 8.1, -2.5, -48.7,
           2.5, 129.3, 46.8, 14.5, 102.5, 32.8, 31.8, 38.4, 69.0, -2.7,
           93.7, 14.2, 4.6, 59.3, 84.6, -23.1, 35.6, 29.8, 38.9, 25.0,
           57.4, 6.2, 34.9, 52.2, -19.9, 26.6, 6.5, -3.8, 15.8, 4.3,
           0.8, 24.1, 28.7, -31.8, 2.7, 21.4, -4.7, 16.8, 32.7, 27.0,
           -12.5, 23.4, 21.9, 2.8, 11.0, 2.4, 29.6, 4.0, 15.8, 25.5]

snp_pct = [10.0, -11.7, 30.9, 11.0, -8.4, 3.9, 14.6, 18.9, -14.8, -26.4,
           37.2, 23.6, -7.4, 6.4, 18.2, 32.3, -5.0, 21.4, 22.4, 6.1,
           31.6, 18.6, 5.1, 16.6, 31.7, -3.1, 30.5, 7.6, 10.1, 1.3,
           37.6, 23.0, 33.4, 28.6, 21.0, -9.1, -11.9, -22.1, 28.7, 10.9,
           4.9, 15.8, 5.5, -37.0, 26.5, 15.1, 2.1, 16.0, 32.4, 13.7,
           1.4, 12.0, 21.8, -4.4, 31.5, 18.4, 28.7, -18.1, 26.3, 25.0]

# 累计指数（起始 = 100）
brk_idx, snp_idx = [100], [100]
for b, s in zip(brk_pct, snp_pct):
    brk_idx.append(brk_idx[-1] * (1 + b / 100))
    snp_idx.append(snp_idx[-1] * (1 + s / 100))
brk_idx, snp_idx = brk_idx[:-1], snp_idx[:-1]   # 60个元素，对齐1965-2024

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(16, 14),
    gridspec_kw={'height_ratios': [3, 2]}
)
fig.suptitle('伯克希尔哈撒韦 vs 标普500（1965–2024）',
             fontsize=20, fontweight='bold', y=0.97)

# --- 上图：累计收益（对数坐标）---
ax1.semilogy(years_brk, brk_idx, color='#1a5276', linewidth=2.2,
             label='伯克希尔', zorder=3)
ax1.semilogy(years_brk, snp_idx, color='#c0392b', linewidth=2.2,
             label='标普500（含股息）', zorder=3)

# 关键节点标注
highlights = [
    (1976, '1976 +129.3%', 18),
    (1985, '1985 哈雷彗星年', -22),
    (1999, '1999 科网泡沫', 16),
    (2008, '2008 金融危机', 16),
]
for yr, note, yoff in highlights:
    i = years_brk.index(yr)
    ax1.annotate(note, xy=(yr, brk_idx[i]), fontsize=8,
                 xytext=(0, yoff), textcoords='offset points',
                 ha='center', color='#1a5276',
                 arrowprops=dict(arrowstyle='->', color='#888', lw=0.7))

ax1.set_ylabel('累计投资价值（起始 $100）', fontsize=13)
ax1.legend(fontsize=13, loc='upper left')
ax1.grid(True, alpha=0.3, which='both')
ax1.set_xlim(1964, 2025)

def y_fmt(x, _):
    if x >= 1e6:
        return f'${x/1e6:.0f}M'
    elif x >= 1e3:
        return f'${x/1e3:.0f}K'
    return f'${x:.0f}'
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(y_fmt))

stats = (
    '60年关键数据\n'
    '━━━━━━━━━━━━━━━━━━━━━━━\n'
    '伯克希尔累计: 5,490,338%  年化 19.9%\n'
    '标普500累计:     38,466%  年化 10.4%\n'
    '跑赢标普 40 年 · 跑输 20 年'
)
ax1.text(0.98, 0.42, stats, transform=ax1.transAxes, fontsize=10,
         va='top', ha='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef9e7',
                   alpha=0.92, edgecolor='#d4ac0d'))

# --- 下图：逐年收益率柱状 ---
bar_w = 0.38
x = np.arange(len(years_brk))
brk_colors = ['#27ae60' if v >= 0 else '#e74c3c' for v in brk_pct]
snp_colors = ['#27ae60' if v >= 0 else '#e74c3c' for v in snp_pct]

ax2.bar(x - bar_w/2, brk_pct, bar_w, color=brk_colors, alpha=0.85,
        label='伯克希尔', zorder=3)
ax2.bar(x + bar_w/2, snp_pct, bar_w, color=snp_colors, alpha=0.50,
        label='标普500', zorder=3)

ax2.set_ylabel('年度收益率 (%)', fontsize=13)
ax2.set_xlabel('年份', fontsize=13)
ax2.set_xticks(x[::5])
ax2.set_xticklabels([str(y) for y in years_brk[::5]], rotation=45)
ax2.axhline(0, color='black', lw=0.5)
ax2.legend(fontsize=12, loc='upper right')
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_xlim(-1, len(years_brk))

plt.tight_layout(rect=[0, 0, 1, 0.95])
path1 = os.path.join(OUT, 'berkshire-performance-1965-2024.png')
fig.savefig(path1, dpi=150, bbox_inches='tight')
print(f'Saved: {path1}')
plt.close()

# ================================================================
# 图2: 巴菲特合伙基金 vs 道指 (1957–1969)
# ================================================================
years_p = list(range(1957, 1970))
dow_pct  = [-8.4, 38.5, 20.0, -6.2, 22.4, -7.6, 20.6, 18.7, 14.2, -15.6, 19.0, 7.7, -11.6]
fund_pct = [10.4, 40.9, 25.9, 22.8, 45.9, 13.9, 38.7, 27.8, 47.2,  20.4, 35.9, 58.8,  6.8]
lp_pct   = [ 9.3, 32.2, 20.9, 18.6, 35.9, 11.9, 30.5, 22.3, 36.9,  16.8, 28.4, 45.6,  5.0]

# 累计指数
fund_idx, dow_idx, lp_idx = [100], [100], [100]
for f, d, l in zip(fund_pct, dow_pct, lp_pct):
    fund_idx.append(fund_idx[-1] * (1 + f/100))
    dow_idx.append(dow_idx[-1]  * (1 + d/100))
    lp_idx.append(lp_idx[-1]    * (1 + l/100))
fund_idx, dow_idx, lp_idx = fund_idx[:-1], dow_idx[:-1], lp_idx[:-1]  # 13个元素，对齐1957-1969

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(14, 12),
    gridspec_kw={'height_ratios': [2, 2]}
)
fig.suptitle('巴菲特合伙基金 vs 道指（1957–1969）',
             fontsize=20, fontweight='bold', y=0.97)

# --- 上图：累计收益 ---
ax1.plot(years_p, fund_idx, color='#1a5276', linewidth=2.5, marker='o',
         markersize=6, label='合伙基金（整体）', zorder=3)
ax1.plot(years_p, lp_idx, color='#2980b9', linewidth=2, marker='s',
         markersize=5, label='有限合伙人', zorder=3)
ax1.plot(years_p, dow_idx, color='#c0392b', linewidth=2.5, marker='^',
         markersize=6, label='道指', zorder=3)

# 填充合伙基金领先区域
ax1.fill_between(years_p, fund_idx, dow_idx, alpha=0.12, color='#1a5276')

ax1.set_ylabel('累计投资价值（起始 $100）', fontsize=13)
ax1.legend(fontsize=12, loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1956, 1970)

def y_fmt2(x, _):
    return f'${x:.0f}'
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(y_fmt2))

stats2 = (
    '13年关键数据\n'
    '━━━━━━━━━━━━━━━━━━━━━━━\n'
    '合伙基金累计: 2,794.6%  年化 29.5%\n'
    '有限合伙人:   1,555.7%  年化 24.0%\n'
    '道指累计:       152.6%  年化  7.4%\n'
    '亏损年度: 0 年（道指 4 年）'
)
ax1.text(0.97, 0.48, stats2, transform=ax1.transAxes, fontsize=10,
         va='top', ha='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#eaf2f8',
                   alpha=0.92, edgecolor='#d4ac0d'))

# --- 下图：逐年收益率 ---
x = np.arange(len(years_p))
bar_w = 0.35

fund_colors = ['#27ae60' if v >= 0 else '#e74c3c' for v in fund_pct]
dow_colors  = ['#27ae60' if v >= 0 else '#e74c3c' for v in dow_pct]

ax2.bar(x - bar_w/2, fund_pct, bar_w, color=fund_colors, alpha=0.85,
        label='合伙基金', zorder=3)
ax2.bar(x + bar_w/2, dow_pct, bar_w, color=dow_colors, alpha=0.50,
        label='道指', zorder=3)

# 在每根柱子上标注数值
for i, (f, d) in enumerate(zip(fund_pct, dow_pct)):
    ax2.text(i - bar_w/2, f + 1.5, f'{f}%', ha='center', va='bottom',
             fontsize=7, color='#1a5276', fontweight='bold')

ax2.set_ylabel('年度收益率 (%)', fontsize=13)
ax2.set_xlabel('年份', fontsize=13)
ax2.set_xticks(x)
ax2.set_xticklabels([str(y) for y in years_p])
ax2.axhline(0, color='black', lw=0.5)
ax2.legend(fontsize=12, loc='upper right')
ax2.grid(True, alpha=0.3, axis='y')

# 标注道指下跌年份（基金仍正收益）
for i, d in enumerate(dow_pct):
    if d < 0:
        ax2.annotate('道指跌\n基金赚', xy=(i, fund_pct[i]),
                     xytext=(25, 15), textcoords='offset points',
                     fontsize=7, color='#c0392b',
                     arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.7))

plt.tight_layout(rect=[0, 0, 1, 0.95])
path2 = os.path.join(OUT, 'partnership-performance-1957-1969.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
print(f'Saved: {path2}')
plt.close()

print('Done!')
